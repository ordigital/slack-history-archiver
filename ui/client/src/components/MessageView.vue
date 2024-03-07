<template>
    <div :class="{ 'message card my-3 mx-2 text-bg-dark': true, 'border-primary': msg.active }" v-if="msg.ts">
        <!-- Message header-->
        <div class="card-header text-muted d-flex justify-content-between">
            <!-- Name and data-->
            <div>
                <h5>{{ msg.user_name }}</h5> 
                <span class="text-muted fs-6 fw-light" v-if="msg.date">{{ msg.date }} in {{msg.channel}}</span>
            </div>
            <!-- Avatar -->
            <div>
                <img :src="msg.avatar" class="img-fluid rounded-circle border" width="54" alt="">
            </div>
        </div>
        <!-- Message Body -->
        <div class="card-body">
            <p class="card-text text-muted">
                <MarkdownRenderer :source="msg.text" :keyword="search" />
            </p>
            <!-- Attachments -->
            <div v-for="a in msg.attachments" :key="a">
              <!-- Link attachment -->
              <div v-if="a.title_link" class="bg-dark border m-2 row rounded attachment-link">
                <div class="col-lg-3 border p-0">
                  <img v-if="a.thumb_url" :src="a.thumb_url" class="img-fluid h-100" alt="">
                  <img v-else :src="a.image_url" class="img-fluid h-100" alt="">
                </div>
                <div class="col-lg-9 p-2">
                  <p><a :href="a.title_link" class="fw-bold text-decoration-none">{{a.title}}</a></p>
                  <p class="text-muted"><small>{{a.text}}</small></p>
                </div>
              </div>
            </div>
        </div>
        <!-- Message Footer -->
        <div v-if="footer" class="card-footer text-body-secondary">
            <div v-if="msg.is_reply">
              <small>This is a reply. You can see it in a 
                <a role="button" class="fw-bold text-decoration-none" @click="$emit('open-message',msg)">thread</a>.
              </small></div>
            <div v-if="msg.reply_count && !msg.active" @click="$emit('open-replies', msg)">
              <small>This message has <a role="button" class="fw-bold text-decoration-none">
                {{msg.reply_count}} replies
              </a></small>
            </div>
        </div>
    </div>
</template>

<script>
import MarkdownRenderer from './MarkdownRenderer.vue';

export default {
  name: 'MessageView',
  props: ['message','footer','search'],
  components: {
    MarkdownRenderer,
  },
  data() {
    return {
      msg: {
        id: '', team: '', channel: '', ts: '', text: '', 
        attachments: '', user_name: '', date: '', avatar: '', email: '',
        is_reply: '', thread_ts: ''
      },
    };
  },
  methods: {
  },
  created() {
    // prop to local variable
    this.msg = this.message;
    // format date
    var d = new Date(this.message['ts']*1000);
    this.msg['date'] = d.getDate() + " " + (d.toLocaleDateString('en-EN', { month: 'long' })) + " " + d.getFullYear() + ", " + d.getHours() + ":" + d.getMinutes();
  },
};
</script>