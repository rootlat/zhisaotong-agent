<template>
   <div class="chat-layout">
      <!-- 侧边栏 -->
      <div class="sidebar">
         <div class="sidebar-header">
            <el-button type="primary" class="new-chat" :loading="creatingSession" :disabled="!canCreateNewSession"
               @click="createSession">
               <ElIcon>
                  <Plus />
               </ElIcon> 新建对话
            </el-button>
         </div>
         <div class="session-list">
            <div v-for="item in sessionList" :key="item.id" class="session-item"
               :class="{ active: item.id === activeSession }" @click="switchSession(item.id)">
               <ElIcon class="session-icon">
                  <ChatDotRound />
               </ElIcon>
               <span class="session-title">{{ item.title }}</span>

               <!-- 单个对话删除按钮 -->
               <div class="delete-btn" @click.stop="deleteSession(item.id)">
                  <ElIcon size="14">
                     <Close />
                  </ElIcon>
               </div>
            </div>
            <div v-if="sessionList.length === 0" class="empty-sessions">
               暂无对话，点击上方新建
            </div>
         </div>
      </div>

      <!-- 主聊天区 -->
      <div class="chat-main">
         <div class="chat-header">
            <div class="title">
               <ElIcon>
                  <Service />
               </ElIcon> 智扫通智能客服
            </div>

            <div class="user-menu" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
               <div class="user-info">
                  <el-avatar :src="userInfo.avatar || 'http://picsum.photos/id/1005/40/40'" :size="36" />
                  <span class="name">{{ userInfo.username }}</span>
                  <ElIcon>
                  </ElIcon>
               </div>
               <div class="logout-dropdown" v-show="showLogout">
                  <!-- 清空所有对话 -->
                  <div class="logout-item clear-all" @click.stop="clearAllSessions">
                     <ElIcon>
                        <Delete />
                     </ElIcon> 清空对话
                  </div>
                  <div class="logout-item" @click="handleLogout">
                     <ElIcon>
                        <SwitchButton />
                     </ElIcon> 退出登录
                  </div>
               </div>
            </div>
         </div>

         <div class="message-box" ref="msgBoxRef" @scroll="handleScroll">
            <div class="message-container">
               <div v-for="msg in messageList" :key="msg.id" class="message-item" :class="msg.role">
                  <div v-if="msg.role === 'user'" class="user-msg">
                     <div class="content">{{ msg.content }}</div>
                     <el-avatar src="http://picsum.photos/id/1005/40/40" class="avatar" :size="36" />
                  </div>
                  <div v-else class="ai-msg">
                     <el-avatar src="http://picsum.photos/id/1/40/40" class="avatar" :size="36" />
                    <div class="content" v-html="formatMessage(msg.content)"></div>
                  </div>
               </div>
            </div>
         </div>

         <div class="input-box">
            <div class="input-wrapper">
               <el-input v-model="inputText" type="textarea" rows="3" placeholder="输入问题，Enter发送，Shift+Enter换行"
                  @keydown="handleKeydown" :disabled="isSending" class="chat-input" />
               <div class="tool-bar">
                  <el-button class="upload-btn" @click="$router.push('/upload')">
                     <ElIcon class="el-icon--left">
                        <Upload />
                     </ElIcon> 上传文件
                  </el-button>
                  <el-button type="primary" class="send-btn" @click="sendMessage" :loading="isSending">
                     发送 <ElIcon>
                        <Right />
                     </ElIcon>
                  </el-button>
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
import {
   Upload, Plus, ChatDotRound, Service, SwitchButton, Right, Close, Delete
} from '@element-plus/icons-vue'
import { ElIcon, ElMessage, ElMessageBox } from 'element-plus'
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import request from '@/utils/request'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const router = useRouter()
const userInfo = ref({ username: '加载中...', avatar: 'http://picsum.photos/id/1005/40/40' })
const showLogout = ref(false)
const msgBoxRef = ref(null)
const inputText = ref('')
const sessionList = ref([])
const activeSession = ref(null)
const messageList = ref([])

let logoutTimer = null
const isSending = ref(false)
const creatingSession = ref(false)
let autoScrollEnabled = true

const LAST_SESSION_KEY = 'chat_last_active_session'

marked.setOptions({
   breaks: false,
   gfm: true,
})

const canCreateNewSession = computed(() => {
   if (activeSession.value && activeSession.value.toString().startsWith('blank_')) return true
   if (!activeSession.value) return false
   return messageList.value.length > 0
})

// --------------- 用户菜单 ---------------
const handleMouseEnter = () => {
   clearTimeout(logoutTimer)
   showLogout.value = true
}
const handleMouseLeave = () => {
   logoutTimer = setTimeout(() => { showLogout.value = false }, 250)
}

// --------------- 滚动 ---------------
let scrollTimer = null
const handleScroll = () => {
   clearTimeout(scrollTimer)
   scrollTimer = setTimeout(() => {
      const box = msgBoxRef.value
      if (!box) return
      const isAtBottom = box.scrollHeight - box.scrollTop - box.clientHeight < 50
      autoScrollEnabled = isAtBottom
   }, 80)
}
const scrollToBottom = () => {
   if (!autoScrollEnabled) return
   nextTick(() => {
      const box = msgBoxRef.value
      if (box) box.scrollTop = box.scrollHeight
   })
}

// --------------- 消息格式化 ---------------
const formatMessage = (content) => {
   if (!content) return ''
   // 转 markdown + 安全过滤
   const html = marked.parse(content)
   return DOMPurify.sanitize(html)
}

// --------------- 保存最后会话 ---------------
const saveLastSession = (id) => {
   localStorage.setItem(LAST_SESSION_KEY, id)
}

// --------------- 会话列表 ---------------
const getSessionList = async () => {
   try {
      const res = await request.get('/chat/session/list')
      sessionList.value = res.data || []

      const lastId = localStorage.getItem(LAST_SESSION_KEY)

      if (lastId) {
         if (lastId.toString().startsWith('blank_')) {
            activeSession.value = lastId
            messageList.value = []
            return
         }
         const exist = sessionList.value.some(s => s.id === lastId)
         if (exist) {
            activeSession.value = lastId
            await getMessageList(activeSession.value)
            return
         }
      }

      if (sessionList.value.length) {
         activeSession.value = sessionList.value[0].id
         await getMessageList(activeSession.value)
      } else {
         createBlankSession()
      }
   } catch (e) {
      ElMessage.error('获取会话列表失败')
   }
}

// --------------- 新建空白会话 ---------------
const createBlankSession = () => {
   const blankId = 'blank_' + Date.now()
   activeSession.value = blankId
   messageList.value = []
   saveLastSession(blankId)
}

// --------------- 新建会话 ---------------
const createSession = async () => {
   if (creatingSession.value) return
   creatingSession.value = true
   try {
      createBlankSession()
   } catch (e) {
      ElMessage.error('创建会话失败')
   } finally {
      creatingSession.value = false
   }
}

// --------------- 切换会话 ---------------
const switchSession = async (id) => {
   if (id === activeSession.value) return
   activeSession.value = id
   saveLastSession(id)

   if (id.toString().startsWith('blank_')) {
      messageList.value = []
      return
   }

   await getMessageList(id)
   autoScrollEnabled = true
   scrollToBottom()
}

// --------------- 获取消息 ---------------
const getMessageList = async (sid) => {
   try {
      const res = await request.get(`/chat/message/list?sessionId=${sid}`)
      messageList.value = res.data || []
      scrollToBottom()
   } catch (e) {
      ElMessage.error('加载消息失败')
   }
}

// --------------- 删除单个会话 ---------------
const deleteSession = async (id) => {
   try {
      await ElMessageBox.confirm('确定要删除该对话吗？删除后无法恢复', '提示', {
         confirmButtonText: '确定',
         cancelButtonText: '取消',
         type: 'warning'
      })

      await request.delete(`/chat/session/delete?sessionId=${id}`)
      ElMessage.success('删除成功')

      sessionList.value = sessionList.value.filter(item => item.id !== id)

      if (activeSession.value === id) {
         if (sessionList.value.length) {
            activeSession.value = sessionList.value[0].id
            await getMessageList(activeSession.value)
         } else {
            createBlankSession()
         }
      }

      saveLastSession(activeSession.value)
   } catch (e) {
      ElMessage.info('已取消')
   }
}

// --------------- 清空所有会话 ---------------
const clearAllSessions = async () => {
   try {
      await ElMessageBox.confirm('确定要清空所有对话吗？清空后无法恢复', '提示', {
         confirmButtonText: '确定清空',
         cancelButtonText: '取消',
         type: 'danger'
      })

      await request.delete('/chat/session/clear-all')
      ElMessage.success('已清空所有对话')

      sessionList.value = []
      createBlankSession()
   } catch (e) {
      ElMessage.info('已取消')
   }
}

// --------------- 键盘发送 ---------------
const handleKeydown = (e) => {
   if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (!isSending.value && inputText.value.trim()) sendMessage()
   }
}

// --------------- 确保会话存在 ---------------
const ensureActiveSession = async () => {
   if (activeSession.value && !activeSession.value.toString().startsWith('blank_')) {
      return activeSession.value
   }

   creatingSession.value = true
   try {
      const res = await request.post('/chat/session/create', { title: '新对话' })
      sessionList.value.unshift(res.data)
      activeSession.value = res.data.id
      saveLastSession(res.data.id)
      return res.data.id
   } catch (e) {
      ElMessage.error('创建会话失败')
      return null
   } finally {
      creatingSession.value = false
   }
}

// --------------- 发送消息 ---------------
const sendMessage = async () => {
   const content = inputText.value.trim()
   if (!content || isSending.value) return

   const sessionId = await ensureActiveSession()
   if (!sessionId) return

   isSending.value = true
   inputText.value = ''

   messageList.value.push({
      id: Date.now(),
      role: 'user',
      content
   })
   scrollToBottom()

   const aiMsgId = Date.now() + 1
   messageList.value.push({
      id: aiMsgId,
      role: 'assistant',
      content: '<div class="thinking-box"><span class="loading"></span> 思考中</div>'
   })

   let fullText = ''

   try {
      const token = localStorage.getItem('token') || ''
      const response = await fetch(
         `/api/chat/stream?sessionId=${sessionId}&content=${encodeURIComponent(content)}`,
         {
            method: 'GET',
            headers: {
               'Authorization': 'Bearer ' + token,
               'Accept': 'text/event-stream',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive'
            }
         }
      )

      if (!response.ok) throw new Error('网络请求异常')
      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
         const { done, value } = await reader.read()
         if (done) break

         const chunk = decoder.decode(value, { stream: true })
         const lines = chunk.split('\n')

         for (const line of lines) {
            if (!line.startsWith('data:')) continue
            const dataStr = line.replace('data:', '').trim()
            if (!dataStr || dataStr === '[DONE]') continue

            try {
               const data = JSON.parse(dataStr)

               if (data.type === 'response') {
                  fullText += data.content || ''
                  const idx = messageList.value.findIndex(m => m.id === aiMsgId)
                  if (idx !== -1) {
                     messageList.value[idx].content = fullText
                  }
                  scrollToBottom()
               }

               if (data.type === 'error') {
                  ElMessage.error(data.content || '服务异常')
                  const idx = messageList.value.findIndex(m => m.id === aiMsgId)
                  if (idx !== -1) {
                     messageList.value[idx].content = '服务异常：' + data.content
                  }
               }

               if (data.type === 'done') {
                  break
               }

            } catch (e) { }
         }
      }

   } catch (e) {
      ElMessage.error('连接失败，请重试')
      const idx = messageList.value.findIndex(m => m.id === aiMsgId)
      if (idx !== -1) {
         messageList.value[idx].content = '回复失败，请稍后重试'
      }
   } finally {
      isSending.value = false

      const item = sessionList.value.find(s => s.id === sessionId)
      if (item) {
         let title = content.trim()
         if (title.length > 18) title = title.slice(0, 18) + '...'
         item.title = title
      }

      await getMessageList(sessionId)
   }
}

// --------------- 退出登录 ---------------
const handleLogout = async () => {
   const { useUserStore } = await import('@/stores/user')
   const userStore = useUserStore()
   userStore.logout()
   localStorage.removeItem('token')
   localStorage.removeItem(LAST_SESSION_KEY)
   ElMessage.success('退出成功')
   router.push('/login')
}

// --------------- 初始化 ---------------
onMounted(async () => {
   const { useUserStore } = await import('@/stores/user')
   const userStore = useUserStore()
   try {
      await userStore.getUserInfo()
      userInfo.value = userStore.userInfo
   } catch (e) {
      ElMessage.error('请登录')
      router.push('/login')
   }
   await getSessionList()
})

onBeforeUnmount(() => {
   clearTimeout(logoutTimer)
})
</script>

<style scoped>
* {
   margin: 0;
   padding: 0;
   box-sizing: border-box;
}

.chat-layout {
   display: flex;
   height: 100vh;
   max-width: 1600px;
   margin: 0 auto;
   background: linear-gradient(135deg, #f5f7fa 0%, #e9edf2 100%);
   font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* ========= 侧边栏 ========= */
.sidebar {
   width: 280px;
   background: rgba(255, 255, 255, 0.92);
   backdrop-filter: blur(2px);
   border-right: 1px solid rgba(0, 0, 0, 0.05);
   display: flex;
   flex-direction: column;
   box-shadow: 2px 0 12px rgba(0, 0, 0, 0.03);
}

.sidebar-header {
   padding: 24px 20px 16px;
   border-bottom: 1px solid #f0f2f5;
}

.new-chat {
   width: 100%;
   background: linear-gradient(135deg, #409eff 0%, #36b0ff 100%);
   border: none;
   border-radius: 40px;
   padding: 12px 0;
   font-weight: 500;
   letter-spacing: 0.5px;
   box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
   transition: all 0.2s ease;
}

.new-chat:hover {
   transform: translateY(-1px);
   box-shadow: 0 6px 16px rgba(64, 158, 255, 0.3);
}

.session-list {
   flex: 1;
   padding: 16px 12px;
   overflow-y: auto;
}

.session-item {
   display: flex;
   align-items: center;
   gap: 12px;
   padding: 12px 16px;
   margin-bottom: 6px;
   border-radius: 14px;
   cursor: pointer;
   transition: all 0.2s ease;
   color: #2c3e50;
   font-size: 14px;
   font-weight: 500;
   position: relative;
}

.session-icon {
   font-size: 16px;
   color: #8c9aaf;
}

.session-item.active .session-icon {
   color: #409eff;
}

.session-item .session-title {
   flex: 1;
   white-space: nowrap;
   overflow: hidden;
   text-overflow: ellipsis;
}

.session-item:hover {
   background: rgba(64, 158, 255, 0.08);
   transform: translateX(2px);
}

.session-item.active {
   background: rgba(64, 158, 255, 0.15);
   color: #409eff;
   box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

.delete-btn {
   width: 22px;
   height: 22px;
   display: flex;
   align-items: center;
   justify-content: center;
   border-radius: 50%;
   color: #999;
   opacity: 0;
   transition: all 0.2s;
}

.session-item:hover .delete-btn {
   opacity: 1;
}

.delete-btn:hover {
   background: #fef0f0;
   color: #f56c6c;
}

.empty-sessions {
   text-align: center;
   color: #a0aaba;
   font-size: 13px;
   margin-top: 40px;
   padding: 0 16px;
}

/* ========= 主聊天区 ========= */
.chat-main {
   flex: 1;
   display: flex;
   flex-direction: column;
   background: #ffffff;
   border-radius: 32px 0 0 32px;
   box-shadow: -4px 0 24px rgba(0, 0, 0, 0.02);
   overflow: hidden;
}

.chat-header {
   height: 70px;
   padding: 0 28px;
   background: #ffffff;
   border-bottom: 1px solid #f0f2f5;
   display: flex;
   align-items: center;
   justify-content: space-between;
}

.title {
   font-size: 18px;
   font-weight: 600;
   background: linear-gradient(135deg, #1e2a3a, #2c3e50);
   -webkit-background-clip: text;
   background-clip: text;
   color: transparent;
   display: flex;
   align-items: center;
   gap: 8px;
}

.user-menu {
   position: relative;
   cursor: pointer;
}

.user-info {
   display: flex;
   align-items: center;
   gap: 10px;
   padding: 6 12px;
   border-radius: 40px;
   transition: background 0.2s;
}

.user-info:hover {
   background: #f5f7fa;
}

.name {
   font-size: 14px;
   font-weight: 500;
   color: #2c3e50;
}

.logout-dropdown {
   position: absolute;
   top: 55px;
   right: 0;
   width: 140px;
   background: #fff;
   border-radius: 20px;
   box-shadow: 0 12px 28px rgba(0, 0, 0, 0.1);
   border: 1px solid #eef2f6;
   z-index: 9999;
   overflow: hidden;
}

.logout-item {
   padding: 12px 18px;
   font-size: 14px;
   color: #f56c6c;
   display: flex;
   align-items: center;
   gap: 10px;
   transition: background 0.2s;
}

.logout-item.clear-all {
   color: #e6a23c;
}

.logout-item:hover {
   background: #fef0f0;
}

/* 消息区域 */
.message-box {
   flex: 1;
   padding: 24px 20px;
   overflow-y: auto;
   background: #fafbfd;
}

.message-container {
   max-width: 900px;
   margin: 0 auto;
}

.message-item {
   margin-bottom: 24px;
   display: flex;
   width: 100%;
   animation: fadeInUp 0.25s ease-out;
}

.message-item.user {
   justify-content: flex-end;
}

.message-item.assistant {
   justify-content: flex-start;
}

.user-msg {
   display: flex;
   align-items: flex-start;
   gap: 12px;
   max-width: 80%;
   flex-direction: row !important;
   margin-left: auto;
}

.ai-msg {
   display: flex;
   align-items: flex-start;
   gap: 12px;
   max-width: 80%;
   flex-direction: row;
   margin-right: auto;
}

/* 消息内容排版 —— 最终完美版 */
.content {
   padding: 14px 20px;
   border-radius: 20px;
   font-size: 15px;
   line-height: 1.6;
   white-space: pre-wrap;
   word-wrap: break-word;
   box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

:deep(.content p) {
   margin: 0 0 4px 0 !important;
}

:deep(.content p:last-child) {
   margin-bottom: 0 !important;
}

:deep(.content ul),
:deep(.content ol) {
   padding-left: 22px !important;
   /* 列表缩进 */
   margin: 4px 0 6px 0 !important;
}

:deep(.content li) {
   margin: 1px 0 !important;
   /* 列表紧凑 */
}

.user-msg .content {
   background: linear-gradient(135deg, #409eff, #36b0ff);
   color: white;
   border-bottom-right-radius: 8px;
}

.ai-msg .content {
   background: #ffffff;
   border: 1px solid #eef2f6;
   color: #2c3e50;
   border-bottom-left-radius: 8px;
}

.avatar {
   flex-shrink: 0;
   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 输入框区域 */
.input-box {
   padding: 20px 28px 28px;
   background: #ffffff;
   border-top: 1px solid #f0f2f5;
}

.input-wrapper {
   max-width: 900px;
   margin: 0 auto;
}

.chat-input :deep(.el-textarea__inner) {
   border-radius: 28px;
   padding: 12px 20px;
   font-size: 15px;
   border: 1px solid #e2e8f0;
   transition: all 0.2s;
   resize: none;
}

.chat-input :deep(.el-textarea__inner):focus {
   border-color: #409eff;
   box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
}

.tool-bar {
   display: flex;
   justify-content: space-between;
   margin-top: 16px;
}

.upload-btn,
.send-btn {
   border-radius: 40px;
   padding: 10px 24px;
   font-weight: 500;
   transition: all 0.2s;
}

.upload-btn {
   background: #f8fafc;
   border-color: #e2e8f0;
   color: #475569;
}

.upload-btn:hover {
   background: #f1f5f9;
   border-color: #cbd5e1;
}

.send-btn {
   background: linear-gradient(135deg, #409eff, #36b0ff);
   border: none;
   box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

.send-btn:hover {
   transform: translateY(-1px);
   box-shadow: 0 6px 14px rgba(64, 158, 255, 0.25);
}

@keyframes fadeInUp {
   from {
      opacity: 0;
      transform: translateY(12px);
   }

   to {
      opacity: 1;
      transform: translateY(0);
   }
}

/* 滚动条 */
.message-box::-webkit-scrollbar {
   width: 6px;
}

.message-box::-webkit-scrollbar-track {
   background: #eef2f6;
   border-radius: 3px;
}

.message-box::-webkit-scrollbar-thumb {
   background: #cbd5e1;
   border-radius: 3px;
}

.session-list::-webkit-scrollbar {
   width: 4px;
}

.session-list::-webkit-scrollbar-thumb {
   background: #cbd5e1;
   border-radius: 4px;
}

@media (max-width: 768px) {
   .sidebar {
      width: 240px;
   }

   .user-msg,
   .ai-msg {
      max-width: 90%;
   }

   .tool-bar {
      flex-wrap: wrap;
      gap: 12px;
   }
}

:deep(.thinking-box) {
   display: inline-flex;
   align-items: center;
   gap: 8px;
   color: #409eff;
   font-size: 15px;
}

:deep(.loading) {
   width: 14px;
   height: 14px;
   border: 2px solid transparent;
   border-top: 2px solid #409eff;
   border-radius: 50%;
   animation: spin 0.8s linear infinite;
}

@keyframes spin {
   0% {
      transform: rotate(0deg);
   }

   100% {
      transform: rotate(360deg);
   }
}
</style>