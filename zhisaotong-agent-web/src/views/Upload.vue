<template>
   <div class="file-manager-page">
      <!-- 顶部标题栏 -->
      <div class="page-header">
         <div class="header-left">
            <el-button text class="back-btn" @click="$router.back()">
               <el-icon>
                  <ArrowLeft />
               </el-icon> 返回
            </el-button>
            <h1>知识文件管理</h1>
         </div>
      </div>

      <!-- 上传区域 -->
      <div class="upload-wrapper">
         <el-upload :http-request="customUpload" multiple :limit="20" drag :show-file-list="false">
            <div class="upload-drag-area">
               <el-icon class="upload-icon">
                  <UploadFilled />
               </el-icon>
               <div class="upload-text">
                  拖拽文件至此处
                  <em>点击选择文件</em>
               </div>
               <div class="upload-tip">支持多文件批量上传</div>
            </div>
         </el-upload>
      </div>

      <!-- 文件列表 -->
      <div class="table-container">
         <div class="table-header">
            <h3>文件列表</h3>
            <div class="table-btns">
               <el-button type="danger" plain @click="handleClearAll" :disabled="fileTable.length === 0">
                  <el-icon>
                     <Delete />
                  </el-icon> 清空所有文件
               </el-button>
               <el-button type="primary" plain @click="getFileList">
                  <el-icon>
                     <Refresh />
                  </el-icon> 刷新列表
               </el-button>
            </div>
         </div>

         <el-table :data="fileTable" border stripe style="width: 100%" row-key="id">
            <el-table-column prop="fileName" label="文件名" min-width="300" />
            <el-table-column label="文件大小" width="150">
               <template #default="scope">
                  {{ formatFileSize(scope.row.fileSize) }}
               </template>
            </el-table-column>
            <el-table-column label="上传时间" width="180">
               <template #default="scope">
                  {{ scope.row.createdAt ? scope.row.createdAt.replace('T', ' ') : '-' }}
               </template>
            </el-table-column>
            <el-table-column prop="status" label="处理状态" width="140">
               <template #default="scope">
                  <el-tag :type="scope.row.status === 3 ? 'success' : scope.row.status === 4 ? 'danger' : 'info'" round>
                     {{
                        scope.row.status === 1
                           ? "已上传"
                           : scope.row.status === 2
                              ? "解析中"
                              : scope.row.status === 3
                                 ? "解析成功"
                                 : "解析失败"
                     }}
                  </el-tag>
               </template>
            </el-table-column>

            <!-- 操作列 -->
            <el-table-column label="操作" width="80" align="center">
               <template #default="scope">
                  <el-button text type="danger" class="del-icon-btn"
                     @click="handleDelete(scope.row.id, scope.row.fileName)">
                     <el-icon>
                        <Close />
                     </el-icon>
                  </el-button>
               </template>
            </el-table-column>
         </el-table>
      </div>
   </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, UploadFilled, Refresh, Delete, Close } from '@element-plus/icons-vue'
import request from '@/utils/request'

const fileTable = ref([])

// 获取文件列表
const getFileList = async () => {
   try {
      const res = await request.get('/file/list')
      fileTable.value = res.data || []
   } catch (err) {
      console.error('获取列表失败：', err)
      ElMessage.error('获取文件列表失败')
   }
}

// 自定义上传
const customUpload = async (params) => {
   const file = params.file
   if (!file || file.size === 0) {
      ElMessage.warning('跳过空文件：' + file.name)
      params.onSuccess()
      return
   }

   const formData = new FormData()
   formData.append('files', file)

   try {
      await request.post('/file/upload', formData, {
         headers: { 'Content-Type': 'multipart/form-data' }
      })
      ElMessage.success('上传成功：' + file.name)
      getFileList()
      params.onSuccess()
   } catch (err) {
      console.error('上传失败：', err)
      ElMessage.error('上传失败：' + file.name)
      params.onError(err)
   }
}

// 删除单个文件
const handleDelete = async (id, fileName) => {
   try {
      await ElMessageBox.confirm(
         '确定要删除文件【' + fileName + '】吗？删除后无法恢复',
         '提示',
         { type: 'warning' }
      )

      await request.delete(`/file/delete/${id}`)
      ElMessage.success('删除成功')
      getFileList()
   } catch (err) {
      if (err !== 'cancel') {
         console.error('删除失败：', err)
         ElMessage.error('删除失败')
      }
   }
}

// 清空所有文件
const handleClearAll = async () => {
   try {
      await ElMessageBox.confirm(
         '确定要清空所有知识文件吗？此操作不可恢复！',
         '警告',
         { type: 'danger', confirmButtonText: '确定清空', cancelButtonText: '取消' }
      )

      await request.delete('/file/clearAll')
      ElMessage.success('已清空所有文件')
      getFileList()
   } catch (err) {
      if (err !== 'cancel') {
         console.error('清空失败：', err)
         ElMessage.error('清空失败')
      }
   }
}

// 格式化文件大小
const formatFileSize = (kb) => {
   if (!kb || kb <= 0) return '0.00 KB'
   const toFixed = (num) => parseFloat(num).toFixed(3)
   if (kb < 1024) return toFixed(kb) + ' KB'
   else if (kb < 1024 * 1024) return toFixed(kb / 1024) + ' MB'
   else return toFixed(kb / 1024 / 1024) + ' GB'
}

onMounted(() => {
   getFileList()
})
</script>

<style scoped>
.file-manager-page {
   width: 100%;
   height: 100vh;
   padding: 28px 32px;
   display: flex;
   flex-direction: column;
   gap: 24px;
   background-color: #f5f7fa;
   box-sizing: border-box;
}

.page-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
}

.header-left {
   display: flex;
   align-items: center;
   gap: 16px;
}

.back-btn {
   font-size: 14px;
   color: #409eff;
}

h1 {
   font-size: 24px;
   font-weight: 600;
   color: #1f2329;
   margin: 0;
}

.upload-wrapper {
   background: #fff;
   border-radius: 12px;
   padding: 20px;
   box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

:deep(.el-upload-dragger) {
   border: 2px dashed #e4e7ed;
   border-radius: 8px;
   transition: all 0.3s;
}

:deep(.el-upload-dragger:hover) {
   border-color: #409eff;
   background-color: #fafbff;
}

.upload-drag-area {
   padding: 40px 0;
   text-align: center;
}

.upload-icon {
   font-size: 50px;
   color: #c0c6cc;
   margin-bottom: 16px;
}

.upload-text {
   font-size: 15px;
   color: #606266;
   margin-bottom: 8px;
}

.upload-tip {
   font-size: 12px;
   color: #909399;
}

.table-container {
   flex: 1;
   display: flex;
   flex-direction: column;
   gap: 16px;
   background: #fff;
   border-radius: 12px;
   padding: 20px;
   box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
   overflow: hidden;
}

.table-header {
   display: flex;
   justify-content: space-between;
   align-items: center;
}

.table-btns {
   display: flex;
   gap: 12px;
}

:deep(.el-table) {
   flex: 1;
}

:deep(.el-upload-list) {
   display: none !important;
}

/* 叉叉删除按钮样式 */
.del-icon-btn {
   font-size: 18px;
   padding: 4px;
}

.del-icon-btn:hover {
   color: #f56c6c;
}
</style>