// Polling-based Chat System (No WebSockets required!)
// Works on PythonAnywhere free tier and all hosting platforms

// Global variables
var playerName = 'Player';
var chatPollInterval = null;
var lastMessageId = 0;
var isChatInitialized = false;
var pollIntervalMs = 4000; // Poll every 4 seconds

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Fetch player info from server to get the real player name
    fetchPlayerInfo().then(function() {
        // Small delay to ensure all DOM elements are ready
        setTimeout(function() {
            initPollingChat();
        }, 300);
    });
});

function fetchPlayerInfo() {
    return new Promise(function(resolve) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/api/player/info', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        if (response.player_name) {
                            playerName = response.player_name;
                            // Also update window.playerName for other scripts
                            window.playerName = playerName;
                        }
                    } catch (e) {
                        // Silently fail on parse error
                    }
                }
                resolve();
            }
        };
        
        xhr.send();
    });
}

function initPollingChat() {
    // Set up chat input handler
    var sendButton = document.getElementById('send-chat');
    var inputField = document.getElementById('chat-input');

    if (sendButton) {
        sendButton.addEventListener('click', function(e) {
            e.preventDefault();
            sendChatMessage();
        });
    }

    if (inputField) {
        inputField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
    
    // Start polling for new messages
    startPolling();
    
    // Update connection status
    updateConnectionStatus(true, 'Connected (polling)');
    
    // Update chat users list to show current user
    updateChatUsersList();
    
    isChatInitialized = true;
}

function startPolling() {
    // Clear any existing interval
    if (chatPollInterval) {
        clearInterval(chatPollInterval);
    }
    
    // Fetch messages immediately
    fetchMessages();
    
    // Start polling interval
    chatPollInterval = setInterval(function() {
        fetchMessages();
    }, pollIntervalMs);
    
}

function stopPolling() {
    if (chatPollInterval) {
        clearInterval(chatPollInterval);
        chatPollInterval = null;
    }
}

function fetchMessages() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/chat/messages?last_id=' + lastMessageId, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                try {
                    var response = JSON.parse(xhr.responseText);
                    if (response.messages && response.messages.length > 0) {
                        // Add new messages to chat
                        response.messages.forEach(function(msg) {
                            addChatMessage(msg.player, msg.message, msg.time_str);
                            lastMessageId = msg.id;
                        });
                    }
                } catch (e) {
                    // Silently fail on parse error
                }
            } else {
                // Silently fail on HTTP error
            }
        }
    };
    
    xhr.send();
}

function sendChatMessage() {
    var inputField = document.getElementById('chat-input');
    if (!inputField) return;
    
    var message = inputField.value.trim();
    if (!message || message.length > 200) {
        showNotification('Message must be 1-200 characters', 'error');
        return;
    }
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/chat/send', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                try {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        inputField.value = '';
                        // Message will appear when fetched via polling
                        showNotification('Message sent!', 'success');
                    } else {
                        showNotification(response.error || 'Failed to send message', 'error');
                    }
                } catch (e) {
                    showNotification('Error sending message', 'error');
                }
            } else {
                showNotification('Error sending message (status: ' + xhr.status + ')', 'error');
            }
        }
    };
    
    var payload = JSON.stringify({
        player_name: playerName,
        message: message
    });
    
    xhr.send(payload);
}

function addChatMessage(player, message, timeStr) {
    var chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) {
        return;
    }
    
    var messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';
    
    // Sanitize content
    var safePlayer = player ? player.replace(/</g, '<').replace(/>/g, '>') : 'Unknown';
    var safeMessage = message ? message.replace(/</g, '<').replace(/>/g, '>') : '';
    var safeTime = timeStr || '';
    
    messageDiv.innerHTML = '<span class="chat-time">[' + safeTime + ']</span> <strong>' + safePlayer + ':</span> ' + safeMessage;
    chatMessages.appendChild(messageDiv);

    // Limit chat messages to prevent overflow
    var maxMessages = 50;
    while (chatMessages.children.length > maxMessages) {
        chatMessages.removeChild(chatMessages.firstChild);
    }

    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function updateConnectionStatus(connected, reason) {
    var indicator = document.getElementById('connection-indicator');
    var text = document.getElementById('connection-text');
    
    if (text) {
        if (connected) {
            if (indicator) {
                indicator.style.color = '#00ff00';
            }
            text.textContent = 'Connected (Polling)';
            text.style.color = '#00ff00';
        } else {
            if (indicator) {
                indicator.style.color = '#ff0000';
            }
            text.textContent = reason || 'Disconnected';
            text.style.color = '#ff0000';
        }
    }
}

function updateChatUsersList() {
    // Update the chat users list to show current user
    var pvpListDiv = document.getElementById('pvp-player-list');
    if (!pvpListDiv) return;
    
    // Show the current player and a note about polling chat
    var safePlayerName = playerName ? playerName.replace(/</g, '<').replace(/>/g, '>') : 'Player';
    
    pvpListDiv.innerHTML = 
        '<div class="user-list-item">' +
            '<strong>👤 ' + safePlayerName + '</strong> (You)' +
        '</div>' +
        '<p style="font-size: 11px; color: #888; margin-top: 10px;">' +
            '💬 Global chat enabled' +
        '</p>' +
        '<p style="font-size: 10px; color: #666;">' +
            'Messages update every 3s' +
        '</p>';
}

function showNotification(message, type) {
    var notification = document.createElement('div');
    notification.className = 'notification notification-' + type;
    notification.textContent = message;
    notification.style.cssText = 'position: fixed; top: 20px; right: 20px; background: ' + 
        (type === 'success' ? '#4CAF50' : type === 'error' ? '#F44336' : '#2196F3') + 
        '; color: white; padding: 10px 20px; border-radius: 5px; z-index: 10000; box-shadow: 0 2px 10px rgba(0,0,0,0.3);';
    document.body.appendChild(notification);

    setTimeout(function() {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Handle command buttons
function handleCommand(command) {
    var inputField = document.getElementById('chat-input');
    if (inputField) {
        inputField.value = command;
        sendChatMessage();
    }
}

// Export functions for global access
window.sendChatMessage = sendChatMessage;
window.handleCommand = handleCommand;
window.updateConnectionStatus = updateConnectionStatus;
