<template>
  <div id="app">




    <div class="container">

      <div class="row mb-4">
        <div class="col">
          <h1 class="text-center">Qualification Task: Question-Answering on Temporal Relations</h1>
        </div>
      </div>

      <nav>
        <div class="nav nav-pills nav-fill" id="nav-tab" role="tablist">
          <a class="nav-item nav-link"
             v-on:click="switch_tab('overview')"
             v-bind:class="{
              'active': show_tab_overview
             }"
          >Overview</a>

          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-event')"
             v-bind:class="{
              'active': show_tab_event
             }"
          >Training Section (Events)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-question')"
             v-bind:class="{
              'active': show_tab_question
             }"
          >Training Section (Questions)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-qa')"
             v-bind:class="{
              'active': show_tab_qa
             }"
          >Training Section (QA)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('test')"
             v-bind:class="{
              'active': show_tab_test
             }"
          >Qualification Test</a>
        </div>
      </nav>

      <div class="container" v-if="show_tab_overview">
        <div class="row"><div class="col-lg-12">
          <div class="card-body">
            <h5 class="card-header">Overview</h5>
            <div class="card-text" style="text-align: left">
              <strong>This is a qualification task for "QA on Temporal Relations" that you can preview <a href="https://qatmr.github.io/" target="_blank">here</a>. Hereafter we refer to the task in that link as the "real task", while referring to this task below as the "qualification task". No matter whether you've worked on the real task or not, the instructions in this qualification task is self-contained, so you're all welcome to work on this qualification task below. </strong><br/><br/>
              <strong>We have launched several pilot studies for the real task and many of you have done pretty well on it. However, we do find some patterns of mistakes in our result, which has motivated us to isolate those typical mistakes out and created this new "qualification task."</strong><br><br>
              <strong>As a heads-up, the real task requires you to label events in text, write temporal relation questions about the text, and then answer your own questions. Therefore, we want you to learn from this qualification task:
                <ul>
                  <li>whether something is an event or not</li>
                  <li>whether a question is about "temporal relations"</li>
                  <li>whether a question-answer pair makes sense to an English speaker</li>
                </ul>
              </strong>
              <strong>For each of the 3 things above, you will first see some instructions and then you will work on an <span style="color:DodgerBlue">"Interactive Training"</span> section, where you'll judge whether an event/question/answer annotation is correct; if you make a mistake there, you will see explanations without any penalty. After finishing your training over these, you will finally see the <span style="color:DodgerBlue">"Qualification Test"</span> section, where you will only know whether you have passed it or not (i.e., we won't tell you whether you're correct on a specific question).</strong><br><br>
              <strong>The qualification task seems long, but most of them are just examples and should be easy to read. In addition, for those who have worked on the real task, it should be very fast to read through and pass the qualification test; for those who have never worked on the real task, reading through the instructions here will save time when you work on the real task. So please be patient and enjoy it!</strong>

            </div>
          </div>

        </div></div>

      </div>

      <div class="container" v-if="show_tab_event">
        <instruction></instruction>
        <a data-toggle="collapse" href="#collapseTrainingEvent" aria-expanded="true" aria-controls="collapseTrainingEvent">
          <h1> Interactive Training 1: Event (click to collapse) </h1>
        </a>
        <div id="collapseTrainingEvent" class="collapse show">
          <p>You will only have several chances to do the qualification test, so please go through these examples carefully before working on the qualification section.</p>
          <question
                  v-for="(item, key) in example_events"
                  v-bind:key="key"
                  v-bind:index="'e'+key.toString()"
                  v-bind:annotation="item"
          >

          </question>
        </div>
      </div>

      <div class="container" v-if="show_tab_question">
        <instruction-questions></instruction-questions>
        <a data-toggle="collapse" href="#collapseTrainingQuestions" aria-expanded="true" aria-controls="collapseTrainingQuestions">
          <h1> Interactive Training 2: Questions (click to collapse) </h1>
        </a>
        <div id="collapseTrainingQuestions" class="collapse show">
          <p>You will only have several chances, so please go through these examples carefully before working on the qualification section.</p>
          <p>Typically you can judge if a question is correct or not purely based on the question itself without the need to see the passage. However, we still present these passages to you for consistency.</p>
          <question
                  v-for="(item, key) in example_questions"
                  v-bind:key="key"
                  v-bind:index="'e'+key.toString()"
                  v-bind:annotation="item"
          >

          </question>
        </div>
      </div>

      <div class="container" v-if="show_tab_qa">
        <instruction-qa></instruction-qa>
        <a data-toggle="collapse" href="#collapseTrainingQA" aria-expanded="true" aria-controls="collapseTrainingQA">
          <h1> Interactive Training 3: Question-Answering (click to collapse) </h1>
        </a>
        <div id="collapseTrainingQA" class="collapse show">
          <p>You will only have several chances, so please go through these examples carefully before working on the qualification section.</p>
          <question
                  v-for="(item, key) in example_qa"
                  v-bind:key="key"
                  v-bind:index="'e'+key.toString()"
                  v-bind:annotation="item"
          >

          </question>
        </div>
      </div>

      <div class="container" v-if="show_tab_test">

        <div v-if="!event_training_passed && can_continue">
          <div class="alert alert-warning" role="alert">
            You have not finished the interactive training section for how to judge events. You can ignore this message if you're sure you don't want to read that anymore (e.g., you have worked on this before).<br>
            <button type="button" class="btn btn-info" v-on:click="switch_tab('training-event')"> Go to Training section for Events</button>
          </div>

        </div>

        <div v-if="!question_training_passed && can_continue">
          <div class="alert alert-warning" role="alert">
            You have not finished the interactive training section for how to judge questions. You can ignore this message if you're sure you don't want to read that anymore (e.g., you have worked on this before).<br>
            <button type="button" class="btn btn-info" v-on:click="switch_tab('training-question')"> Go to Training section for Question</button>
          </div>

        </div>

        <div v-if="!qa_training_passed && can_continue">
          <div class="alert alert-warning" role="alert">
            You have not finished the interactive training section for how to judge if an answer is correct to a question. You can ignore this message if you're sure you don't want to read that anymore (e.g., you have worked on this before).<br>
            <button type="button" class="btn btn-info" v-on:click="switch_tab('training-qa')"> Go to Training section for QA</button>
          </div>
        </div>

        <h1>Qualification test</h1>
        <div v-if="loading && !error_occurred" class="alert alert-warning" role="alert">
          LOADING...If this message persists, you can refresh this page and see.
        </div>
        <div v-if="can_continue && !loading && !error_occurred">
          <question
                  v-for="(item, key) in test_events"
                  v-bind:key="key"
                  v-bind:index="'q'+key.toString()"
                  v-bind:annotation="item"
          >
          </question>
          <question
                  v-for="(item, key) in test_questions"
                  v-bind:key="key"
                  v-bind:index="'q'+key.toString()"
                  v-bind:annotation="item"
          >
          </question>
          <question
                  v-for="(item, key) in test_qa"
                  v-bind:key="key"
                  v-bind:index="'q'+key.toString()"
                  v-bind:annotation="item"
          >
          </question>
        </div>

        <div v-if="ever_checked && has_response && !error_occurred">
          <div role="alert" class="alert"
              v-bind:class="{
                'alert-warning': can_continue,
                'alert-success': qualified,
                'alert-danger': blacklisted,
              }"
          >
            <span v-html="msg_response"></span><br>
          </div>
        </div>

        <div v-if="qualified">
          <question
                  v-for="(item, key) in error_qids"
                  v-bind:key="key"
                  v-bind:index="key"
                  v-bind:annotation="response_history[key]"
          >
          </question>
        </div>

        <div v-if="!error_occurred">
          <div class="alert" role="alert"
               v-bind:class="{
                'alert-warning': can_continue,
                'alert-success': qualified,
                'alert-danger': blacklisted,
              }">
            <span v-html="msg_qualified_blacklisted"></span><br>
          </div>
        </div>

        <div v-if="error_occurred">
          <div class="alert alert-danger" role="alert">
            Sorry. Something unexpected has happened. Please refresh this page and see. If the problem isn't resolved, please contact the owner of this task.<br>
          </div>
        </div>

        <button
                type="button"
                class="btn btn-primary btn-lg btn-block"
                v-on:click="submitTestResultToUs"
                v-if="!qualified && !blacklisted &&!error_occurred"
                :disabled="!can_check || frozen"
        >Check your answers {{remaining_timer}}</button>

        <button
                type="button"
                class="btn btn-primary btn-lg btn-block"
                v-if="!error_occurred"
                v-on:click="submitHit"
                :disabled="!can_submit || frozen"
                data-balloon-pos="up"
                aria-label="(1) Empty submissions are considered spamming and will lead to rejection of your submissions. (2) The bonus will be paid typically within two weeks."
        >Submit response [pay: ${{this.basepay | currency}} + ${{ this.bonus | currency}} = ${{ total_payment |
          currency}}] {{remaining_timer}}</button>

        <div>
          <form
                  name='mturk_form'
                  method='post'
                  id='mturk-external-submit-form'
                  v-bind:action="mturk_params.turkSubmitTo"
                  type='hidden'
          >
            <input type='hidden' name='assignmentId' id='assignmentId' v-bind:value="mturk_params.assignmentId"/>
            <input type='hidden' name='bonusAmt' id='bonusAmt' v-bind:value="bonus"/>
            <input name="generated_answers_event" type="hidden" v-model="generated_answers.event">
            <input name="generated_answers_question" type="hidden" v-model="generated_answers.question">
            <input name="generated_answers_qa" type="hidden" v-model="generated_answers.qa">
            <!--<input type='submit' class="btn btn-success btn-sm" id='submitButton' name="submitButton" value='Click here to submit HIT'>-->
          </form>

          <div class="alert alert-danger" role="alert" v-if="show_submission_alert">
            There's an error in submission.
          </div>
        </div>

      </div>
      <nav>
        <div class="nav nav-pills nav-fill" role="tablist">
          <a class="nav-item nav-link"
             v-on:click="switch_tab('overview')"
             v-bind:class="{
              'active': show_tab_overview
             }"
          >Overview</a>

          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-event')"
             v-bind:class="{
              'active': show_tab_event
             }"
          >Training Section (Events)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-question')"
             v-bind:class="{
              'active': show_tab_question
             }"
          >Training Section (Questions)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('training-qa')"
             v-bind:class="{
              'active': show_tab_qa
             }"
          >Training Section (QA)</a>
          <a class="nav-item nav-link"
             v-on:click="switch_tab('test')"
             v-bind:class="{
              'active': show_tab_test
             }"
          >Qualification Test</a>
        </div>
      </nav>



    </div>


  </div>
</template>

<script>
import Question from './components/Question.vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import queryString from "query-string";
import Vue from 'vue';
import _ from 'lodash';
import Papa from "papaparse";
import axios from "axios";
import Instruction from "./components/Instruction";
import InstructionsOnQuestions from "@/components/InstructionsOnQuestions";
import InstructionsQA from "@/components/InstructionsQA";
import 'balloon-css';

export default {
  name: 'app',
  components: {
    Question,
    'instruction': Instruction,
    'instruction-questions': InstructionsOnQuestions,
    'instruction-qa': InstructionsQA
  },
  data: function(){
    return {
        frozen: true,
        seconds_remain: 60,
        seconds_to_wait: 60,
        response_history: {

        },

        active_tab: "overview",

        example_events: {},
        example_questions: {},
        example_qa: {},
        test_events: {},
        test_questions: {},
        test_qa: {},
        mturk_params: {
          assignmentId: "",
          hitId: "",
          turkSubmitTo: "",
          workerId: "",
          isPreview: true,
        },
        generated_answers: {
          qa: "",
          event: "",
          question: "",
        },
        show_submission_alert: false,

        training_example_max: 3,
        number_of_qual_questions_event: 5,
        number_of_qual_questions_question: 5,
        number_of_qual_questions_qa: 10,

        blacklisted: false,
        qualified: false,
        remainingAttempts: -1,
        attempts: 100,
        verify_response: {},
        bonus: 0,
        basepay: 2.0,
        bonus_per_attempt: 1.0,
        passpay: 5.0,
        error_qids: {},

        backend_endpoint: "",
        loading: false,
        error_occurred: false
    }
  },

  filters: {
    currency: function(value){
      return value.toFixed(2);
    }
  },

  computed: {
    ever_checked: function(){
      return this.attempts>0 || this.qualified;
    },

    show_tab_overview: function(){
      return this.active_tab === "overview"
    },

    show_tab_event: function(){
      return this.active_tab === "training-event"
    },

    show_tab_question: function(){
      return this.active_tab === "training-question"
    },

    show_tab_qa: function(){
      return this.active_tab === "training-qa"
    },

    show_tab_test: function(){
      return this.active_tab === "test"
    },

    event_training_passed: function(){
      return _.every(this.example_events, q => {return q.picked !== null})
    },
    question_training_passed: function(){
      return _.every(this.example_questions, q => {return q.picked !== null})
    },
    qa_training_passed: function(){
      return _.every(this.example_qa, q => {return q.picked !== null})
    },


    can_check: function(){
      // for (let i = 0; i < this.questions.length; i++){
      //   if (this.question[i].picked === null){
      //     return false;
      //   }
      // }
      //
      // return true;
      return !this.blacklisted && _.every(this.test_events, q => {return q.picked !== null}) && _.every(this.test_questions, q => {return q.picked !== null}) && _.every(this.test_qa, q => {return q.picked !== null});
    },

    can_submit: function(){
      // for (let i = 0; i < this.questions.length; i++){
      //   if (this.question[i].picked === null){
      //     return false;
      //   }
      // }
      //
      // return true;

      return this.ever_checked && !this.error_occurred;
    },

    total_payment: function(){
      return this.basepay + this.bonus;
    },

    msg_response: function(){
      if(Object.keys(this.verify_response).length > 0){
        if(this.qualified){
          return "Congratulations. You have passed the qualification test. Please do check the mistakes you may have made during the test and correct your misunderstandings if any. If you have any questions, please take a screenshot of your mistakes and send an email to us. If everything looks good, you can submit this hit using the wide blue &lt;Submit Response&gt; button below.";
        }
        else{
          let msg = "Sorry. You failed to pass the test, but you'll receive $"+this.bonus_per_attempt+" bonus for any additional attempts.<br>";
          msg+= "Judging events: "+this.verify_response['event_mistake_cnt']+" mistake(s). "
                  +(this.verify_response['event_qualify'] === "1" ? "<span style='color:green'>[passed]</span>" : "<span style='color:red'>[failed]</span>") + "<br>";
          msg+= "Judging questions: "+this.verify_response['question_mistake_cnt']+" mistake(s). "
                  +(this.verify_response['question_qualify'] === "1" ? "<span style='color:green'>[passed]</span>" : "<span style='color:red'>[failed]</span>") + "<br>";
          msg+= "Judging answers: "+this.verify_response['qa_mistake_cnt']+" mistake(s). "
                  +(this.verify_response['qa_qualify'] === "1" ? "<span style='color:green'>[passed]</span>" : "<span style='color:red'>[failed]</span>") + "<br>";
          msg+= "You may modify your answers above and re-evaluate it. You can also refresh this page using the refresh button of your web browser to get another set of random questions."
          return msg;
        }
      }
      else{
        return "Error occurred."
      }
    },

    msg_qualified_blacklisted: function(){
      if(this.blacklisted){
        return "You have reached the maximum number of attempts. You cannot try this hit anymore. However, you can still submit your hit and get paid for this task.";
      }
      if(this.qualified)
        return "You've passed this qualification task. Please go to https://worker.mturk.com/mturk/preview?groupId=3NIW7VZHBKSBBAEF7LKRYYA931AGOA and continue working on it. We will take a look at your submission there and then contact you with substantially more hits. Please do check your mistakes above because that will increase your chance of passing the new task.";
      // not qualified but not blacklisted yet
      return "You still have " + this.remainingAttempts + " remaining chance(s). Every attempt will reward you $" + this.bonus_per_attempt + ". If you pass it, you will receive in total $"+this.passpay+".";
    },

    local_debug_mode: function(){
      return this.backend_endpoint=== "127.0.0.1:9050";
    },

    protocol: function(){
      return this.local_debug_mode? "http://" : "https://";
    },

    has_response: function(){
      return Object.keys(this.verify_response).length > 0;
    },

    can_continue: function(){
      return !this.qualified && !this.blacklisted;
    },

    remaining_timer: function(){
      if(this.seconds_remain>0)
        return "(enabled in "+this.seconds_remain+" seconds)";
      return "";
    }
  },

  async mounted() {
      const parsed_query_string = queryString.parse(location.search);
      console.log(parsed_query_string);
      
      let assignmentId = parsed_query_string.assignmentId;
      if(assignmentId === null || assignmentId === undefined){
        assignmentId = "TestAssignmentId";
      }

      this.number_of_qual_questions_event = 'nEvent' in parsed_query_string ?  parseInt(parsed_query_string.nEvent): 0;
      this.number_of_qual_questions_question = 'nQuestion' in parsed_query_string ?  parseInt(parsed_query_string.nQuestion): 0;
      this.number_of_qual_questions_qa = 'nQA' in parsed_query_string ?  parseInt(parsed_query_string.nQA): 0;
      this.basepay = 'basepay' in parsed_query_string ?  parseFloat(parsed_query_string.basepay): 2.0;
      this.bonus_per_attempt = 'bonusRate' in parsed_query_string ?  parseFloat(parsed_query_string.bonusRate): 1.0;
      this.passpay = 'passpay' in parsed_query_string ?  parseFloat(parsed_query_string.passpay): 5.0;
      this.active_tab = 'tab' in parsed_query_string ? parsed_query_string.tab : "overview";
      if(this.active_tab!=="overview"
      &&this.active_tab!=="training-event"
      &&this.active_tab!=="training-question"
      &&this.active_tab!=="training-qa"
      &&this.active_tab!=="test"){
        this.active_tab = "overview";
      }

      this.backend_endpoint = 'backend_endpoint' in parsed_query_string ?  parsed_query_string.backend_endpoint: "127.0.0.1:9050";

      if (assignmentId === "ASSIGNMENT_ID_NOT_AVAILABLE"){
        console.log("Preview mode.");
        this.mturk_params.isPreview = true;
      }

      const hitId = parsed_query_string.hitId;
      const turkSubmitTo = parsed_query_string.turkSubmitTo;
      let workerId = parsed_query_string.workerId;
      if(workerId === null || workerId === undefined){
        workerId = "TestUser";
      }

      this.mturk_params.turkSubmitTo = turkSubmitTo + "/mturk/externalSubmit";
      this.mturk_params.workerId = workerId;
      this.mturk_params.hitId = hitId;
      this.mturk_params.assignmentId = assignmentId;

      const self = this;

      const worker_verify_url = this.protocol + this.backend_endpoint + "/can_work";
      console.log("checking eligibility at: " + worker_verify_url);
      axios.get(worker_verify_url, {
        params: {
          worker: workerId
        }
      })
      .then(function (response) {
        console.log(response.data);
        self.blacklisted = response.data.blacklisted;
        self.qualified = response.data.qualified;
        self.remainingAttempts = response.data.remainingAttempts;
        self.attempts = response.data.attempts;

        self.bonus = self.bonus_per_attempt * (self.attempts-1);
        if(self.qualified){
          // self.bonus += self.bonus_per_attempt * (self.remainingAttempts+1);
          self.bonus = self.passpay - self.basepay;
        }
        if(self.bonus<0)
          self.bonus = 0;
      })
      .catch(function (error) {
        console.log(error);
        self.error_occurred = true;
      });

      try{
        // const resp = await fetch("./training.csv");
        // console.log(resp.body);
        Papa.parse("./training-event.csv", {
          download: true,
          header: true,
          complete: function(results) {
            console.log("Finished:", results.data);
            // const data = _.slice(results.data, 0, 3);
            const data = results.data;
            _.each(data, (example, idx) => {
              example.question_id = "training-event-" + idx;
              example.candidates = ['y','n'];
              example.picked = null;
              self.$set(self.example_events, example.question_id ,example);
            })
          }
        })


        Papa.parse("./training-question.csv", {
          download: true,
          header: true,
          complete: function(results) {
            console.log("Finished:", results.data);
            // const data = _.slice(results.data, 0, 3);
            const data = results.data;
            _.each(data, (example, idx) => {
              example.question_id = "training-question-" + idx;
              example.candidates = ['y','n'];
              example.picked = null;
              self.$set(self.example_questions, example.question_id ,example);
            })
          }
        })


        Papa.parse("./training-qa.csv", {
          download: true,
          header: true,
          complete: function(results) {
            console.log("Finished:", results.data);
            // const data = _.slice(results.data, 0, 3);
            const data = results.data;
            _.each(data, (example, idx) => {
              example.question_id = "training-qa-" + idx;
              example.candidates = ['y','n'];
              example.picked = null;
              self.$set(self.example_qa, example.question_id ,example);
            })
          }
        })

        /**
         * Reading testing data.
         */
        this.load_test_csvs();


      }catch (e) {
        console.log(e);
      }
    const update_remain_time_timer = setInterval(
            function(){
              self.seconds_remain -= 1;
              if (self.seconds_remain <= 0){
                self.frozen = false;
                clearInterval(update_remain_time_timer);
              }
            }, 1000);
  },

  methods: {

    save_response_history: function(annotations){
      for (const qid in annotations){
        const annotation = annotations[qid];
        this.$set(this.response_history, qid, _.cloneDeep(annotation))
      }
    },

    load_test_csvs: function(){
      const self = this;
      self.test_events = {};
      self.test_questions = {};
      self.test_qa = {};
      if(!this.has_response || this.verify_response['event_qualify'] === '0') {
        Papa.parse("./test-event-public.csv", {
          download: true,
          header: true,
          error: function () {
            self.error_occurred = true;
          },
          complete: function (results) {
            console.log("Finished loading testing data:", results.data);
            let data = _.map(results.data, (example, idx) => {
              if (example.question_id === null || example.question_id === undefined) {
                return null;
              }
              example._id = "testing-event-" + idx;
              example.candidates = ['y', 'n'];
              example.picked = null;

              example.EventCorrect = null;
              example.QuestionCorrect = null;
              example.QACorrect = null;
              example.Explanation = null;
              return example;
            });
            console.log("Test event csv (original):");
            console.log(Object.keys(data).length);
            data = _.filter(data, (x) => {
              return x !== null
            });
            console.log("Test event csv (after filter):");
            console.log(Object.keys(data).length);
            data = _.sampleSize(data, self.number_of_qual_questions_event);
            console.log("Test event csv (after sample):");
            console.log(Object.keys(data).length);

            _.each(data, (example, idx) => {
              self.$set(self.test_events, example.question_id, example)
            })
          }
        });
      }

      if(!this.has_response || this.verify_response['question_qualify'] === '0') {
        Papa.parse("./test-question-public.csv", {
          download: true,
          header: true,
          error: function () {
            self.error_occurred = true;
          },
          complete: function (results) {
            console.log("Finished loading testing data:", results.data);

            let data = _.map(results.data, (example, idx) => {
              if (example.question_id === null || example.question_id === undefined) {
                return null;
              }
              example._id = "testing-question-" + idx;
              example.candidates = ['y', 'n'];
              example.picked = null;

              example.EventCorrect = null;
              example.QuestionCorrect = null;
              example.QACorrect = null;
              example.Explanation = null;
              return example;
            });
            console.log("Test question csv (original):");
            console.log(Object.keys(data).length);
            data = _.filter(data, (x) => {
              return x !== null
            });
            console.log("Test question csv (after filter):");
            console.log(Object.keys(data).length);
            data = _.sampleSize(data, self.number_of_qual_questions_question);
            console.log("Test question csv (after sample):");
            console.log(Object.keys(data).length);

            _.each(data, (example, idx) => {
              self.$set(self.test_questions, example.question_id, example)
            })
          }
        });
      }

      if(!this.has_response || this.verify_response['qa_qualify'] === '0') {
        Papa.parse("./test-qa-public.csv", {
          download: true,
          header: true,
          error: function () {
            self.error_occurred = true;
          },
          complete: function (results) {
            console.log("Finished loading testing data:", results.data);

            let data = _.map(results.data, (example, idx) => {
              if (example.question_id === null || example.question_id === undefined) {
                return null;
              }

              example._id = "testing-qa-" + idx;
              example.candidates = ['y', 'n'];
              example.picked = null;

              example.EventCorrect = null;
              example.QuestionCorrect = null;
              example.QACorrect = null;
              example.Explanation = null;
              return example;
            });

            console.log("Test qa csv (original):");
            console.log(Object.keys(data).length);
            data = _.filter(data, (x) => {
              return x !== null
            });
            console.log("Test qa csv (after filter):");
            console.log(Object.keys(data).length);
            data = _.sampleSize(data, self.number_of_qual_questions_qa);
            console.log("Test qa csv (after sample):");
            console.log(Object.keys(data).length);

            _.each(data, (example, idx) => {
              self.$set(self.test_qa, example.question_id, example)
            })
          }
        });
      }
    },
    switch_tab: function(tab){
      this.active_tab = tab;
    },
    submitTestResultToUs: function(){
      this.generated_answers.event = JSON.stringify(this.test_events);
      this.generated_answers.question = JSON.stringify(this.test_questions);
      this.generated_answers.qa = JSON.stringify(this.test_qa);

      this.save_response_history(this.test_events);
      this.save_response_history(this.test_questions);
      this.save_response_history(this.test_qa);

      const post_data = {
        "events": this.generated_answers.event,
        "questions": this.generated_answers.question,
        "qa": this.generated_answers.qa,
        "workerId": this.mturk_params.workerId,
        "assignmentId": this.mturk_params.assignmentId,
        "turkSubmitTo": this.mturk_params.turkSubmitTo
      };

      const post_config = {
        headers: {'Access-Control-Allow-Origin': '*'}
      };

      const verify_endpoint = this.protocol + this.backend_endpoint + "/verify";
      this.loading = true;
      const self = this;
      axios.post(verify_endpoint, post_data, post_config).then(data => {
        console.log(data);
        self.verify_response = data.data;
        self.blacklisted = self.verify_response['blacklisted'] === "1";
        self.qualified = self.verify_response['final_qualify'] === "1";
        self.remainingAttempts = parseInt(self.verify_response['remainingAttempts']);
        self.attempts = parseInt(self.verify_response['attempts']);
        self.bonus = self.bonus_per_attempt * (parseInt(self.verify_response['attempts'])-1);
        if(self.qualified){
          self.bonus = self.passpay - self.basepay;
        }
        self.error_qids = self.verify_response['errors_qid'];

        for (const qid in self.error_qids){
          const correct_ans = self.error_qids[qid];
          const correct_ans_test = correct_ans === "y" ? "yes" : "no";
          if (qid.startsWith("qa-")){
              self.$set(self.response_history[qid], "QACorrect", correct_ans);
              // self.$set(self.response_history[qid], "Explanation", "The correct answer is " + correct_ans_test);
              self.$set(self.response_history[qid], "Explanation", self.verify_response['errors_explanations'][qid]);
          }

          if (qid.startsWith("event-")){
            self.$set(self.response_history[qid], "EventCorrect", correct_ans);
            // self.$set(self.response_history[qid], "Explanation", "The correct answer is " + correct_ans_test);
            self.$set(self.response_history[qid], "Explanation", self.verify_response['errors_explanations'][qid]);

          }

          if (qid.startsWith("question-")){
            self.$set(self.response_history[qid], "QuestionCorrect", correct_ans);
            // self.$set(self.response_history[qid], "Explanation", "The correct answer is " + correct_ans_test);
            self.$set(self.response_history[qid], "Explanation", self.verify_response['errors_explanations'][qid]);

          }
        }

        if(self.qualified){
          // self.bonus += self.bonus_per_attempt * (self.remainingAttempts+1);
          self.bonus = self.passpay - self.basepay;
        }
        else{
          self.load_test_csvs();
          self.seconds_remain = self.seconds_to_wait;
          self.frozen = true;
          const update_remain_time_timer = setInterval(
                  function(){
                    self.seconds_remain -= 1;
                    if (self.seconds_remain <= 0){
                      self.frozen = false;
                      clearInterval(update_remain_time_timer);
                    }
                  }, 1000);
        }
        if(self.bonus<0){
          self.bonus = 0;
        }
      }).catch(error => {
        self.error_occurred = true;
        console.log(error);
      });
      this.loading = false;
    },

    submitHit: function(){
      if(this.local_debug_mode){
        console.log("Local testing mode. Not submitting to mturk.");
        return;
      }
      Vue.nextTick(function () {
        document.getElementById('mturk-external-submit-form').submit();
      });
    },
  },

}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.nav-item.active{
  /*color: red !important;*/
  border-bottom-style: solid !important;
  border-bottom: 0px red !important;
  cursor: pointer;
}

.nav-item{
  /*color: red !important;*/
  border-bottom: 2px grey !important;
  border-bottom-style: dotted !important;

  cursor: pointer;
}

button:disabled{
  cursor: not-allowed;
}

</style>
