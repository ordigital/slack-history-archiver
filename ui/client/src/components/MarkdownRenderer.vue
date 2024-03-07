<template>
    <div v-html="rewrite(source,keyword)" />
</template>
  
  <script setup lang="ts">
  import MarkdownIt from "markdown-it";
  import MarkdownItHighlightjs from "markdown-it-highlightjs";


  const markdown = new MarkdownIt().use(MarkdownItHighlightjs, {
    exclude: ['delphi'],
    
    },
  );


    const languages = ['python', 'javascript', 'css', 'html', 'bash'];

    function rewrite(markdownText,keyword) {
        const regex = /```\s*(.*?)\n/g;
        const matches = markdownText.match(regex);

        if (matches) {
            for (const match of matches) {
            const language = match.match(/^\s*(.*?)\s*/)[1];

            if (!languages.includes(language)) {
                markdownText = markdownText.replace(match, `\`\`\` ${language}\n`);
            }
            }
        }

        // highlight keyword
        markdown.renderer.rules.text = function(tokens, idx) {
          const text = tokens[idx].content;
          return text.replace(new RegExp(`${keyword}`, 'gi'), function(matchedWord){
            return `<span class="text-bg-warning">${matchedWord}</span>`;
          });
        };

        var text = markdown.render(markdownText);
        return text;
    }

  defineProps({
    source: {
      type: String,
      default: ""
    },
    keyword: {
      type: String,
      default: ""
    }
  });
  </script>