<template>
  <!--Passage,Event,EventCorrect,Question,QuestionCorrect,QA,QACorrect,Explanation-->
  <div
    class="row"
  >
      <div
          class="col-12 question-card"

      >
        <div
          class="card mt-2"
          v-bind:class="{
            'is-event-card': is_event_question,
            'is-question-card': is_question_question,
            'is-qa-card': is_qa_question,
          }"

        >
          <!--<h5 class="card-header">Featured</h5>-->
          <div class="card-body">
            <h5 class="card-title annotation-passage"><span v-html="annotation.Passage"></span></h5>
            <div class="card-text">
              <hr>
              <div v-if="annotation.Event !== ''">

                <p>
                   Is the <span class="event">"{{annotation.Event}}"</span> highlighted in the passage a correct event?
                </p>


                <div
                        class="form-check form-check-inline"
                        v-for="(resp, idx) in annotation.candidates"
                        v-bind:key="idx"
                >
                  <input class="form-check-input"
                         type="radio"
                         v-bind:name="'rg-' + index"
                         v-bind:value="resp"
                         v-model="annotation.picked"
                         v-bind:class="{
                          'is-valid': is_correct_answer_event && has_correct_answer_event && has_picked_answer,
                          'is-invalid': is_wrong_answer_event && has_correct_answer_event && has_picked_answer
                       }"
                  >
                  <label class="form-check-label" >{{render_radio_text(resp)}}</label>
                </div>

                <div class="alert alert-danger" role="alert" v-if="is_wrong_answer_event && has_correct_answer_event && has_picked_answer">
                  {{"Incorrect. " + annotation.Explanation}}
                </div>
                <div class="alert alert-success" role="alert" v-else-if="!is_wrong_answer_event && has_correct_answer_event && has_picked_answer">
                  Correct. Good job!
                </div>


              </div>

              <div v-if="annotation.Question !== ''">
                <p>
                  Is <b>{{annotation.Question}}</b> a good temporal relation question?
                </p>

                <div
                        class="form-check form-check-inline"
                        v-for="(resp, idx) in annotation.candidates"
                        v-bind:key="idx"
                >
                  <input class="form-check-input"
                         type="radio"
                         v-bind:name="'rg-' + index"
                         v-bind:value="resp"
                         v-model="annotation.picked"
                         v-bind:class="{
                          'is-valid': is_correct_answer_question && has_correct_answer_question && has_picked_answer,
                          'is-invalid': is_wrong_answer_question && has_correct_answer_question && has_picked_answer
                       }"
                  >
                  <label class="form-check-label" >{{render_radio_text(resp)}}</label>
                </div>

                <div class="alert alert-danger" role="alert" v-if="is_wrong_answer_question && has_picked_answer && has_correct_answer_question">
                  {{"Incorrect. " + annotation.Explanation}}
                </div>
                <div class="alert alert-success" role="alert" v-else-if="!is_wrong_answer_question && has_picked_answer && has_correct_answer_question">
                  Correct. Good job!
                </div>
              </div>

              <div v-if="annotation.QA !== ''">
                <p>
                  <strong>Question:</strong> {{get_question}}
                </p>
                <p>
                  <strong>Answer Candidate:</strong> {{get_answer}}
                </p>
                <p>
                  Is the answer correct: {{annotation.answer}}
                </p>



                <div
                        class="form-check form-check-inline"
                        v-for="(resp, idx) in annotation.candidates"
                        v-bind:key="idx"
                >
                  <input class="form-check-input"
                         type="radio"
                         v-bind:name="'rg-' + index"
                         v-bind:value="resp"
                         v-model="annotation.picked"
                         v-bind:class="{
                          'is-valid': is_correct_answer_qa && has_picked_answer && has_correct_answer_qa,
                          'is-invalid': is_wrong_answer_qa && has_picked_answer && has_correct_answer_qa
                       }"
                  >
                  <label class="form-check-label" >{{render_radio_text(resp)}}</label>
                </div>

                <div v-if="has_correct_answer_qa">
                  <div class="alert alert-danger" role="alert" v-if="is_wrong_answer_qa && has_picked_answer && has_correct_answer_qa">
                    {{"Incorrect. " + annotation.Explanation}}
                  </div>
                  <div class="alert alert-success" role="alert" v-else-if="!is_wrong_answer_qa && has_picked_answer && has_correct_answer_qa">
                    Correct. Good job!
                  </div>
                </div>

              </div>


            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'Question',
  props: {
    annotation: {
      type: Object,
      required: true,
    },
    index: {
      type: String,
      required: true,
    },
  },
  computed: {

    is_event_question: function(){
      return this.annotation.Event !== '' && this.annotation.Event !== null && this.annotation.Event !== undefined;
    },
    is_question_question: function(){
      return this.annotation.Question !== '' && this.annotation.Question !== null && this.annotation.Question !== undefined;
    },
    is_qa_question: function(){
      return this.annotation.QA !== '' && this.annotation.QA !== null && this.annotation.QA !== undefined;
    },


    has_picked_answer: function(){
      return this.annotation.picked !== null;
    },

    is_correct_answer: function(){
      return this.is_correct_answer_qa || this.is_correct_answer_event || this.is_correct_answer_question;
    },

    is_wrong_answer_qa: function(){
      return this.annotation.picked !== this.annotation.QACorrect;
    },
    is_correct_answer_qa: function(){
      return this.annotation.picked === this.annotation.QACorrect;
    },
    has_correct_answer_qa: function(){
      return this.annotation.QACorrect !== null && this.annotation.QACorrect !== "";
    },

    
    is_wrong_answer_question: function(){
      return this.annotation.picked !== this.annotation.QuestionCorrect;
    },
    is_correct_answer_question: function(){
      return this.annotation.picked === this.annotation.QuestionCorrect;
    },
    has_correct_answer_question: function(){
      return this.annotation.QuestionCorrect !== null && this.annotation.QuestionCorrect !== "";
    },


    is_wrong_answer_event: function(){
      return  this.annotation.picked !== this.annotation.EventCorrect;
    },
    is_correct_answer_event: function(){
      return this.annotation.picked === this.annotation.EventCorrect;
    },
    has_correct_answer_event: function(){
      return this.annotation.EventCorrect !== null && this.annotation.EventCorrect !== "";
    },

    get_question: function(){
      return this.annotation.QA.split("?")[0].trim()+"?";
    },
    get_answer: function(){
      return this.annotation.QA.split("?")[1].trim();
    }
  },
  watch: {
    annotation() {
      this.$emit('input', this.annotation);
    }
  },

  methods: {
    render_radio_text(value){
      if (value === 'y'){
        return "Yes";
      }

      if (value === 'n'){
        return "No";
      }
    }
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.question-card span.event{
  color: red;
}

.card.is-event-card{
  border-color: deepskyblue;
  border-style: solid;
  border-width: 2px;
}

.card.is-question-card{
  border-color: firebrick;
  border-style: solid;
  border-width: 2px;
}

.card.is-qa-card{
  border-color: yellow;
  border-style: solid;
  border-width: 2px;
}

</style>
