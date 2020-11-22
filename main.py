from flask import Flask
from flask import Flask, request, jsonify
import csv
from flask_cors import CORS
import json
import pprint
import boto3
import redis
import datetime as dt



pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)
CORS(app)

# qualify: 10000
# otherwise: number of attempts
max_attempted_failures = 3
event_acc_threshold = 0.8
question_acc_threshold = 0.8
qa_acc_threshold = 0.8
combined_acc_threshold = 0.8


def create_mturk_clients():
    MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    MTURK_PROD = 'https://mturk-requester.us-east-1.amazonaws.com'
    access_key_info = open('../accessKeys.csv').readlines()
    access_key, secret_access_key = access_key_info[-1].strip().split(",")
    client_prod = boto3.client('mturk',
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_access_key,
                               region_name='us-east-1',
                               endpoint_url=MTURK_PROD)
    client_sandbox = boto3.client('mturk',
                                  aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_access_key,
                                  region_name='us-east-1',
                                  endpoint_url=MTURK_SANDBOX)

    access_key_info = open('../accessKeys-allennlp.csv').readlines()
    access_key, secret_access_key = access_key_info[-1].strip().split(",")
    client_prod2 = boto3.client('mturk',
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_access_key,
                               region_name='us-east-1',
                               endpoint_url=MTURK_PROD)
    return client_prod, client_prod2, client_sandbox


client_prod, client_prod2, client_sandbox = create_mturk_clients()
db_failures = redis.Redis(host='localhost', port=6379, db=0)  # number of failures for each worker
db_qualified_workers = redis.Redis(host='localhost', port=6379, db=1)  # qualified
db_responses = redis.Redis(host='localhost', port=6379, db=2)

def retrieve_gold_answers():
    data = {}
    explanation = {}
    with open("./private/test-event.csv") as input_fd:
        csv_reader = csv.DictReader(input_fd)
        for row in csv_reader:
            qid = row['question_id']
            ans = row['EventCorrect']
            exp = row['Explanation']
            data[qid] = ans
            explanation[qid] = exp

    with open("./private/test-qa.csv") as input_fd:
        csv_reader = csv.DictReader(input_fd)
        for row in csv_reader:
            qid = row['question_id']
            ans = row['QACorrect']
            exp = row['Explanation']
            data[qid] = ans
            explanation[qid] = exp

    with open("./private/test-question.csv") as input_fd:
        csv_reader = csv.DictReader(input_fd)
        for row in csv_reader:
            qid = row['question_id']
            ans = row['QuestionCorrect']
            exp = row['Explanation']
            data[qid] = ans
            explanation[qid] = exp
    return data, explanation


gold_ans, gold_explanation = retrieve_gold_answers()
print('----gold ans----')
print(gold_ans)


def get_answers(annotation_obj):
    return {x: y['picked'] for x, y in annotation_obj.items()}


@app.route('/can_work', methods=['GET'])
def can_work():
    worker = request.args.get('worker')
    qualified = True if int(redis_get_or_default(db_qualified_workers, worker, 0)) == 1 else False
    attempts = int(redis_get_or_default(db_failures, worker, 0)) if worker != "bad_user" else 10000
    blacklisted = False if attempts < max_attempted_failures else True
    remainingAttempts = (max_attempted_failures - attempts) if not blacklisted else 0
    ret = json.dumps({
        "attempts": attempts,
        "remainingAttempts": remainingAttempts,
        "blacklisted": blacklisted,
        "qualified": qualified
    })
    print(ret)
    return ret


@app.route('/verify', methods=['POST'])
def verify_response():
    content = request.json
    turkSubmitTo = content['turkSubmitTo']
    print("Received annotation.")

    all_responses = {}

    ans_qa = json.loads(content['qa'])
    qa_correct_count = 0.0
    qa_total_count = 0.0
    for qid, ans in get_answers(ans_qa).items():
        all_responses[qid] = ans
        qa_total_count += 1.0
        if ans == gold_ans[qid]:
            qa_correct_count += 1.0

    ans_question = json.loads(content['questions'])
    question_correct_count = 0.0
    question_total_count = 0.0
    for qid, ans in get_answers(ans_question).items():
        all_responses[qid] = ans
        question_total_count += 1.0
        if ans == gold_ans[qid]:
            question_correct_count += 1.0

    ans_event = json.loads(content['events'])
    event_correct_count = 0.0
    event_total_count = 0.0
    for qid, ans in get_answers(ans_event).items():
        all_responses[qid] = ans
        event_total_count += 1.0
        if ans == gold_ans[qid]:
            event_correct_count += 1.0

    print(event_correct_count, event_total_count)
    print(question_correct_count, question_total_count)
    print(qa_correct_count, qa_total_count)

    workerId = content['workerId']
    print(f"workerId: {workerId}")

    assignmentId = content['assignmentId']
    print(f"assignmentId: {assignmentId}")

    result = verify_response_helper(event_correct_count, event_total_count,
                                    question_correct_count, question_total_count,
                                    qa_correct_count, qa_total_count)
    result['blacklisted'] = "0"

    if result['final_qualify'] == "1":
        print(redis_get_or_default(db_qualified_workers, workerId, "0"))
        db_qualified_workers.set(workerId, "1")
        print(redis_get_or_default(db_qualified_workers, workerId, "0"))
        give_qualification(turkSubmitTo, workerId)
    else:
        if db_failures.incr(workerId) >= max_attempted_failures:
            blacklist(turkSubmitTo, workerId)
            result['blacklisted'] = "1"
    result['attempts'] = str(int(redis_get_or_default(db_failures, workerId, 0)))
    result['remainingAttempts'] = str(max_attempted_failures - int(redis_get_or_default(db_failures, workerId, 0)))

    db_response_key = f"{assignmentId}-{workerId}"
    if result['final_qualify'] != "1":
        db_response_key += "-"+result['attempts']
    print(f"db_response_key {db_response_key}")

    db_response_log = {
        "all_responses":  all_responses,
        "time":  dt.datetime.now().timestamp(),
        "turkSubmitTo": turkSubmitTo,
        "workerId": workerId
    }

    db_responses.set(db_response_key, json.dumps(db_response_log))

    result['errors_qid'] = {}
    result['errors_explanations'] = {}
    if result['final_qualify'] == '1':
        errors_qid_set = get_all_error_history_of_worker(workerId)
        result['errors_qid'] = {x:gold_ans[x] for x in errors_qid_set}
        result['errors_explanations'] = {x:gold_explanation[x] for x in errors_qid_set}
        print("----errors_qid----")
        print(result['errors_qid'])

    print('----result----')
    print(result)
    print(json.dumps(all_responses, indent=4, sort_keys=True))
    return result


def redis_get_or_default(redis, key, default_val):
    val = redis.get(key)
    if val is None:
        return default_val
    return val


def get_all_error_history_of_worker(worker_id):
    error_qid_set = {}
    for key in db_responses.scan_iter("*"+worker_id+"*"):
        responses = json.loads(db_responses.get(key))
        if 'all_responses' not in responses:
            continue
        responses = responses['all_responses']
        for qid, ans in responses.items():
            if ans != gold_ans[qid]:
                error_qid_set[qid] = gold_ans[qid]
    return error_qid_set


def verify_response_helper(event_correct_count, event_total_count,
                           question_correct_count, question_total_count,
                           qa_correct_count, qa_total_count):
    if event_total_count>0:
        acc_event = 1.0 * event_correct_count / event_total_count
    else:
        acc_event = 0
    if question_total_count>0:
        acc_question = 1.0 * question_correct_count / question_total_count
    else:
        acc_question = 0
    if qa_total_count>0:
        acc_qa = 1.0 * qa_correct_count / qa_total_count
    else:
        acc_qa = 0
    if event_total_count + question_total_count + qa_total_count > 0:
        acc = 1.0 * (event_correct_count + question_correct_count + qa_correct_count) / (
                event_total_count + question_total_count + qa_total_count)
    else:
        acc = 0
    event_qualify = acc_event >= event_acc_threshold if event_total_count>0 else True
    question_qualify = acc_question >= question_acc_threshold if question_total_count>0 else True
    qa_qualify = acc_qa >= qa_acc_threshold if qa_total_count>0 else True
    combined_qualify = acc >= combined_acc_threshold if (event_total_count + question_total_count + qa_total_count > 0) else True
    final_qualify = event_qualify and question_qualify and qa_qualify and combined_qualify
    return {'final_qualify': "1" if final_qualify else "0",
            'event_qualify': "1" if event_qualify else "0",
            'question_qualify': "1" if question_qualify else "0",
            'qa_qualify': "1" if qa_qualify else "0",
            'combined_qualify': "1" if combined_qualify else "0",
            'event_mistake_cnt': str(event_total_count - event_correct_count),
            'question_mistake_cnt': str(question_total_count - question_correct_count),
            'qa_mistake_cnt': str(qa_total_count - qa_correct_count)}


def blacklist(turkSubmitTo, workerid):
    # prod qual type id: 37V1PG7CDJHIR6N5FNKQLDI1XO2NH9
    # sandbox qual type id: 3HN7640Z3RB5CS65NDER59BX6JETSU
    if turkSubmitTo == "https://www.mturk.com/mturk/externalSubmit":
        grant_qualification_to_workers(client_prod, '37V1PG7CDJHIR6N5FNKQLDI1XO2NH9', [workerid])
        grant_qualification_to_workers(client_prod2, '3QTDD8KTB5ABJE6J1AVWGHEY0H7HVS', [workerid])
    elif turkSubmitTo == "https://workersandbox.mturk.com/mturk/externalSubmit":
        grant_qualification_to_workers(client_sandbox, '3HN7640Z3RB5CS65NDER59BX6JETSU', [workerid])
    else:
        print(f"Testing: Blacklisting {workerid}.")


def grant_qualification_to_workers(client, qual_id, work_ids):
    for wid in work_ids:
        response = client.associate_qualification_with_worker(
            QualificationTypeId=qual_id,
            WorkerId=wid,
            IntegerValue=1,
            SendNotification=False
        )
        print(f'{wid} qualified for qualification type {qual_id}')


def give_qualification(turkSubmitTo, workerid):
    # real qualification type id: 385F8X38STIHS6EO52XQ2TFV6C0L03
    # sandbox qualification type id: 3VQGW0Q62SLNWSTPFMNFBBNT2YDNU3
    if turkSubmitTo == "https://www.mturk.com/mturk/externalSubmit":
        grant_qualification_to_workers(client_prod, '385F8X38STIHS6EO52XQ2TFV6C0L03', [workerid])
        grant_qualification_to_workers(client_prod2, '36H5CYL7CRU5TSXXA1QV4ENBKXMCB8', [workerid])
    elif turkSubmitTo == "https://workersandbox.mturk.com/mturk/externalSubmit":
        grant_qualification_to_workers(client_sandbox, '3VQGW0Q62SLNWSTPFMNFBBNT2YDNU3', [workerid])
    else:
        print(f"Testing: Giving qualification to {workerid}.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 80
    app.run(host='0.0.0.0', port=port)
