<template>
  <div class="chat-content">
    <!-- 顶部助手提示 -->
    <div class="chat-header">
      <div class="assistant-info">
        <div class="assistant-avatar">
          <img src="@/assets/bot-avatar.png" alt="assistant" />
        </div>
        <div class="assistant-message">您好，我是 智能助手，您可以向我提出 智能助手 使用问题。</div>
      </div>
    </div>

    <!-- 推荐内容区域 -->
    <div class="recommend-section">
      <div class="recommend-title">为您推荐</div>
      <div class="recommend-list">
        <div class="recommend-item" v-for="i in 3" :key="i">
          <div class="item-icon">
            <i class="icon-document"></i>
          </div>
          <div class="item-content">
            <div class="item-title">推进数字学生水利建设</div>
            <div class="item-desc">聚焦合同问题进展如何？</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 聊天消息列表 -->
    <div class="message-list">
      <!-- 用户消息 -->
      <div class="message-item user">
        <div class="message-content">
          <div class="message-text">各单位年度立项数统计？</div>
        </div>
        <div class="message-avatar">
          <img src="@/assets/user-avatar.png" alt="user" />
        </div>
      </div>

      <!-- 助手消息 -->
      <div class="message-item assistant">
        <div class="message-avatar">
          <img src="@/assets/bot-avatar.png" alt="assistant" />
        </div>
        <div class="message-content">
          <div class="message-text">
            这个文本的主题是"各单位年度立项数统计"，看起来像一个询问或通知，涉及各个单位在一年内计划后的项目数量的统计。
          </div>
          <div class="message-actions">
            <button class="action-btn">
              <i class="icon-copy"></i>
            </button>
            <button class="action-btn">
              <i class="icon-refresh"></i>
            </button>
            <button class="action-btn">
              <i class="icon-thumbs-up"></i>
            </button>
            <button class="action-btn">
              <i class="icon-thumbs-down"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-section">
      <div class="input-container">
        <textarea
          class="message-input"
          placeholder="请输入您想要查询的内容......"
          rows="3"
        ></textarea>
        <div class="input-actions">
          <div class="left-actions">
            <button class="action-btn">
              <i class="icon-attachment"></i>
            </button>
          </div>
          <div class="right-actions">
            <button class="send-btn">发 送</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped lang="scss">
.chat-content {
  flex: 1 1 0%;
  height: calc(100% - 20px); // 减去父元素底部padding
  display: flex;
  flex-direction: column;
  background: #fff;

  .chat-header {
    padding: 16px 24px;
    border-bottom: 1px solid #eaedf1;

    .assistant-info {
      display: flex;
      align-items: center;
      gap: 12px;

      .assistant-avatar {
        width: 40px;
        height: 40px;
        border-radius: 20px;
        overflow: hidden;
        background: #e6f4ff;
        display: flex;
        align-items: center;
        justify-content: center;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }

      .assistant-message {
        font-size: 14px;
        color: #1d2129;
      }
    }
  }

  .recommend-section {
    padding: 16px 24px;

    .recommend-title {
      font-size: 16px;
      color: #1d2129;
      margin-bottom: 16px;
      font-weight: 500;
    }

    .recommend-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;

      .recommend-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px;
        background: #f7f9fb;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          background: #e6f4ff;
          transform: translateY(-2px);
        }

        .item-icon {
          width: 40px;
          height: 40px;
          border-radius: 8px;
          background: #e6f4ff;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #1677ff;
        }

        .item-content {
          flex: 1;
          min-width: 0;

          .item-title {
            font-size: 14px;
            color: #1d2129;
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }

          .item-desc {
            font-size: 12px;
            color: #86909c;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }
        }
      }
    }
  }

  .message-list {
    flex: 1;
    padding: 24px;
    overflow-y: auto;

    .message-item {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;

      &.user {
        flex-direction: row-reverse;

        .message-content {
          align-items: flex-end;
        }

        .message-text {
          background: #e6f4ff;
          border-radius: 8px 2px 8px 8px;
        }
      }

      .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 20px;
        overflow: hidden;
        flex-shrink: 0;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }

      .message-content {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: 80%;

        .message-text {
          padding: 12px 16px;
          background: #f7f9fb;
          border-radius: 2px 8px 8px 8px;
          font-size: 14px;
          color: #1d2129;
          line-height: 1.6;
        }

        .message-actions {
          display: flex;
          gap: 8px;

          .action-btn {
            padding: 4px;
            background: none;
            border: none;
            cursor: pointer;
            color: #86909c;
            transition: all 0.3s;

            &:hover {
              color: #1677ff;
            }
          }
        }
      }
    }
  }

  .input-section {
    padding: 16px 24px;
    border-top: 1px solid #eaedf1;

    .input-container {
      background: #f7f9fb;
      border-radius: 8px;
      padding: 12px;

      .message-input {
        width: 100%;
        border: none;
        background: none;
        resize: none;
        outline: none;
        font-size: 14px;
        color: #1d2129;
        line-height: 1.6;

        &::placeholder {
          color: #86909c;
        }
      }

      .input-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;

        .action-btn {
          padding: 6px;
          background: none;
          border: none;
          cursor: pointer;
          color: #86909c;
          transition: all 0.3s;

          &:hover {
            color: #1677ff;
          }
        }

        .send-btn {
          padding: 6px 20px;
          background: #1677ff;
          border: none;
          border-radius: 4px;
          color: white;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s;

          &:hover {
            background: #4096ff;
          }
        }
      }
    }
  }
}
</style>
