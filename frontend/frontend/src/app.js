const chatContainer = document.getElementById("chat-container");
const messageForm = document.getElementById("message-form");
const userInput = document.getElementById("user-input");
const articleContent = document.getElementById("article-content");
const articleSection = document.getElementById("article-section");
const newChatBtn = document.getElementById("new-chat-btn");


// Create a message bubble
function createMessageBubble(content, sender = "user") {
  const wrapper = document.createElement("div");
  wrapper.classList.add("mb-6", "flex", "items-start", "space-x-3", "p-4");

  // Avatar
  const avatar = document.createElement("div");
  avatar.classList.add(
      "w-10",
      "h-10",
      "rounded-full",
      "flex-shrink-0",
      "flex",
      "items-center",
      "justify-center",
      "font-bold",
      "text-white"
  );

  if (sender === "assistant") {
      avatar.classList.add("bg-gradient-to-br", "from-pink-200", "to-blue-400");
      avatar.textContent = "🤖";
  } else {
      avatar.classList.add("bg-gradient-to-br", "from-blue-300", "to-blue-600");
      avatar.textContent = "ME";
  }

  // Bubble
  const bubble = document.createElement("div");
  bubble.classList.add(
      "max-w-full",
      "md:max-w-2xl",
      "p-3",
      "rounded-lg",
      "whitespace-pre-wrap",
      "leading-relaxed",
      "shadow-sm"
  );

  if (sender === "assistant") {
    bubble.classList.add("bg-blue-600", "text-white");
  } else {
    bubble.classList.add("bg-blue-50", "text-gray-900");
  }

  bubble.textContent = content;

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  return wrapper;
}

// Extract economic terms from the assistant's response
function extractEconomicTerms(response) {
    const terms = [];
    const lines = response.split('\n');
    for (const line of lines) {
        const match = line.match(/\d+\.\s+([^:]+):/);
        if (match) {
            terms.push(match[1].trim());
        }
    }
    return terms;
}

// Display article content with highlighted terms
function displayArticleContent(content, economicTerms = []) {
  articleContent.innerHTML = '';
  const textContent = document.createElement("div");
  textContent.classList.add("text-gray-800", "leading-relaxed", "whitespace-pre-line");
  
  // Show the article section when there's content
  articleSection.classList.remove("hidden");
  
  if (economicTerms.length > 0) {
      // Highlight economic terms with blue background and better contrast
      let highlightedContent = content;
      economicTerms.forEach(term => {
          const regex = new RegExp(`(${term})`, 'gi');
          highlightedContent = highlightedContent.replace(
              regex, 
              '<span class="bg-blue-100 text-blue-800 px-1 py-0.5 rounded font-medium">$1</span>'
          );
      });
      textContent.innerHTML = highlightedContent;
  } else {
      textContent.textContent = content;
  }
  
  articleContent.appendChild(textContent);
}

// Scroll to bottom
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Simulate assistant response with backend integration
async function getAssistantResponse(userMessage) {
    try {
        const response = await fetch("http://localhost:8000/findword", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Extract economic terms from the response
        const economicTerms = extractEconomicTerms(data.reply);
        
        // Display the article content with highlighted terms
        if (data.article_content) {
            displayArticleContent(data.article_content, economicTerms);
        }
        
        return data.reply || "No response from backend";
    } catch (error) {
        console.error("Error communicating with the backend:", error);
        return "Sorry, there was an error processing your request.";
    }
}

newChatBtn.addEventListener("click", () => {
  // Clear chat container
  chatContainer.innerHTML = "";
  
  // Clear article section
  articleContent.innerHTML = "";
  articleSection.classList.add("hidden");
  
  // Clear input
  userInput.value = "";
});

// Handle form submission
messageForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // User message
    chatContainer.appendChild(createMessageBubble(message, "user"));
    userInput.value = "";
    scrollToBottom();

    // Assistant response
    const response = await getAssistantResponse(message);
    chatContainer.appendChild(createMessageBubble(response, "assistant"));
    scrollToBottom();
});