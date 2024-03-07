<template>
  <div class="row m-3">
    <div class="col-12">
      <h1 class="p-3 text-danger">⛃ Slack History Archive</h1>
    </div>

    <!-- Channels list -->
    <div class="col-lg-2 p-3">
      <form class="">
        <div class="input-group mb-3">
          <span :class="{ 'input-group-text': true, 'bg-primary': channel === 'search' }" id="search">search</span>
          <input type="text" class="form-control" id="search_i" aria-label="Search" aria-describedby="search" @keyup="search">
        </div>
      </form>
      <ul class="list-group">
        <div v-for="name in channels" :key="name">
          <button type="button" v-if="name == channel" class="list-group-item list-group-item-action active" @click="getChat(name)">{{ name }}</button>
          <button type="button" v-else class="list-group-item list-group-item-action" @click="getChat(name)">{{ name }}</button>
        </div>
      </ul>
    </div>

    <!-- Messages list -->
    <div :class="{'col-lg-6': replies.length > 0, 'col-lg-10': replies.length < 1, 'p-0': true }">
      <div class="container" v-if="messages">
        <div id="messages" v-for="message in messages" :key="message.ts">
          <Message :message=message :footer=true :search=search_field  @open-replies="openReplies" @open-message="openThread" />
        </div>
        <div class="more text-center my-3">
          <button role="button" class="btn btn-primary"  
            @click="loadMore" 
            :disabled="moreDisabled">
            <span v-if="moreDisabled">there are no more messages</span>
            <span v-else>load more messages</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Replies list -->
    <div v-if="replies.length > 0" class="border-start border-dark col-lg-4 p-0 position-fixed bg-dark overflow-y-scroll" style="z-index: 1000; right:0; top: 0; height: 100vh;">
      <div class="container">
        <button type="button" class="btn-close mt-2 border rounded-circle" aria-label="Close" @click="closeReplies"></button>
        <div id="replies" v-for="reply in replies" :key="reply.ts">
          <Message :message=reply />
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import Message from './MessageView.vue';
import { debounce } from 'lodash';

export default {
  name: 'ChatView',
  components: {
        Message
  },
  data() {
    return {
      path: 'http://localhost:5001/', // flask api url
      limit: 10,            // loaded messages limit
      offset: 0,            // offset for loaded messages
      channel: '',          // current channel
      channels: [],         // channels list
      messages: [],         // loaded messages
      search_field: '',     // search field content
      replies: [],          // message replies
      moreDisabled: false,  // more button
    };
  },
  methods: {
    async getData(url,variable,append=null) {
      if(append==1) this.offset += this.limit;
      var path = this.path + url;
      await axios.get(path)
        .then((res) => { 
          // Replace messages
          if(!append) { 
            this.offset = 0; 
            this.replies = []
            this[variable] = res.data; 
          }
          // Add messagess
          else { 
            if(res.data.length > 0) {
              this[variable] = this[variable].concat(res.data); }
          }
          if(variable=='messages') {
            if(res.data.length < this.limit) this.moreDisabled = true; else this.moreDisabled = false;
          }
          
        })
        .catch((error) => { console.error(error); });
    },
    // Get channels list
    async getChannels() {
      await this.getData('channels','channels');
    },
    // Load chat messages
    async getChat(name) {
      // set channel name
      this.channel = name;
      // clear search input
      document.getElementById('search_i').value = '';
      this.search_field = '';
      // get messages
      await this.getData('chat/' + name + '/' + this.limit + '/0', 'messages');
      this.offset += 10;
    },
    // On search typing event
    async search(event) {
      this.search_field = event.target.value;
      if (this.search_field.length >= 3) {
        this.channel = 'search';
        await this.getData('search/' + this.search_field + '/' + this.limit + '/0', 'messages');
      }
    },
    // Load more messages
    async loadMore() {
      if(this.channel == 'search') 
        { await this.getData('search/' + this.search_field + '/' + this.limit + '/' + this.offset, 'messages',1); }
      else 
        { 

          await this.getData('chat/' + this.channel + '/' + this.limit + '/' + this.offset, 'messages', 1); 
        }
    },
    // Open replies in sidebar
    openReplies(data) {
      this.replies = [ JSON.parse(JSON.stringify(data)) ];
      this.replies = this.replies.concat(this.replies[0].replies);
      this.replies[0].replies = [];
      this.replies[0].active = 1;
    },
    // Flush active replies
    closeReplies() {
      this.replies = []
    },
    // Open main thread from searched reply
    async openThread(data) {
      await this.getData('message/' + data.thread_ts,'replies');
      this.replies = this.replies.concat(this.replies[0].replies);
      for (let i = 0; i < this.replies.length; i++) {
        if (this.replies[i].ts === data.ts) {
          this.replies[i].active = 1;
          break;
        }
      }
      this.replies[0].replies = [];
    }
  },
  // Wait until search begin when typing
  mounted() {
    this.search = debounce(this.search, 500);
  },
  // Load channels list and fist channel messages at start
  async created() {
    try {
        await this.getChannels();
        this.getChat(this.channels[0]);
    } catch (error) {
        console.error('Error fetching channels:', error);
    }
  },
};
</script>


