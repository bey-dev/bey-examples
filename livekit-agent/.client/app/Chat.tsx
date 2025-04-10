import type { ChatMessage, ChatOptions } from '@livekit/components-core';
import * as React from 'react';
import { useMaybeLayoutContext, useRoomContext } from '@livekit/components-react'
import type { MessageFormatter } from '@livekit/components-react'
import { ChatEntry } from '@livekit/components-react'
import { useChat } from '@livekit/components-react'
import { ChatToggle } from '@livekit/components-react'
import { ChatCloseIcon } from '@livekit/components-react'
import clsx from 'clsx'

/** @internal */
export function cloneSingleChild(
    children: React.ReactNode | React.ReactNode[],
    props?: Record<string, any>,
    key?: any,
  ) {
    return React.Children.map(children, (child) => {
      // Checking isValidElement is the safe way and avoids a typescript
      // error too.
      if (React.isValidElement(child) && React.Children.only(children)) {
        if (child.props.class) {
          // make sure we retain classnames of both passed props and child
          props ??= {};
          props.class = clsx(child.props.class, props.class);
          props.style = { ...child.props.style, ...props.style };
        }
        return React.cloneElement(child, { ...props, key });
      }
      return child;
    });
  }
/** @public */
export interface ChatProps extends React.HTMLAttributes<HTMLDivElement>, ChatOptions {
  messageFormatter?: MessageFormatter;
}

/**
 * The Chat component adds a basis chat functionality to the LiveKit room. The messages are distributed to all participants
 * in the room. Only users who are in the room at the time of dispatch will receive the message.
 *
 * @example
 * ```tsx
 * <LiveKitRoom>
 *   <Chat />
 * </LiveKitRoom>
 * ```
 * @public
 */
export function Chat({
  messageFormatter,
  messageDecoder,
  messageEncoder,
  channelTopic,
  ...props
}: ChatProps) {
  const inputRef = React.useRef<HTMLInputElement>(null);
  const ulRef = React.useRef<HTMLUListElement>(null);

  const chatOptions: ChatOptions = React.useMemo(() => {
    return { messageDecoder, messageEncoder, channelTopic };
  }, [messageDecoder, messageEncoder, channelTopic]);

  const {  chatMessages, isSending, send } = useChat(chatOptions);

  const layoutContext = useMaybeLayoutContext();
  const lastReadMsgAt = React.useRef<ChatMessage['timestamp']>(0);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    console.log('handleSubmit');
    if (inputRef.current && inputRef.current.value.trim() !== '') {
      if (sendText) {
        await sendText(inputRef.current.value);
        inputRef.current.value = '';
        inputRef.current.focus();
      }
    }
  }

  const room = useRoomContext();

  const sendText = React.useCallback(async (message: string) => {
      if (!room?.localParticipant) return;

      try {
          console.log('Sending text message:', message);
          const info = await room.localParticipant.sendText(message, {
              topic: 'lk.chat'
          });
          console.log('Text message sent:', info);
      } catch (e) {
          console.error('Failed to send message:', e);
      }
  }, [room]);

  React.useEffect(() => {
    if (ulRef) {
      ulRef.current?.scrollTo({ top: ulRef.current.scrollHeight });
    }
  }, [ulRef, chatMessages]);

  React.useEffect(() => {
    if (!layoutContext || chatMessages.length === 0) {
      return;
    }

    if (
      layoutContext.widget.state?.showChat &&
      chatMessages.length > 0 &&
      lastReadMsgAt.current !== chatMessages[chatMessages.length - 1]?.timestamp
    ) {
      lastReadMsgAt.current = chatMessages[chatMessages.length - 1]?.timestamp;
      return;
    }

    const unreadMessageCount = chatMessages.filter(
      (msg) => !lastReadMsgAt.current || msg.timestamp > lastReadMsgAt.current,
    ).length;

    const { widget } = layoutContext;
    if (unreadMessageCount > 0 && widget.state?.unreadMessages !== unreadMessageCount) {
      widget.dispatch?.({ msg: 'unread_msg', count: unreadMessageCount });
    }
  }, [chatMessages, layoutContext?.widget]);

  return (
    <div {...props} className="lk-chat">
      <div className="lk-chat-header">
        Messages
        {layoutContext && (
          <ChatToggle className="lk-close-button">
            <ChatCloseIcon />
          </ChatToggle>
        )}
      </div>

      <ul className="lk-list lk-chat-messages" ref={ulRef}>
        {props.children
          ? chatMessages.map((msg, idx) =>
              cloneSingleChild(props.children, {
                entry: msg,
                key: msg.id ?? idx,
                messageFormatter,
              }),
            )
          : chatMessages.map((msg, idx, allMsg) => {
              const hideName = idx >= 1 && allMsg[idx - 1].from === msg.from;
              // If the time delta between two messages is bigger than 60s show timestamp.
              const hideTimestamp = idx >= 1 && msg.timestamp - allMsg[idx - 1].timestamp < 60_000;

              return (
                <ChatEntry
                  key={msg.id ?? idx}
                  hideName={hideName}
                  hideTimestamp={hideName === false ? false : hideTimestamp} // If we show the name always show the timestamp as well.
                  entry={msg}
                  messageFormatter={messageFormatter}
                />
              );
            })}
      </ul>
      <form className="lk-chat-form" onSubmit={handleSubmit}>
        <input
          className="lk-form-control lk-chat-form-input"
          disabled={isSending}
          ref={inputRef}
          type="text"
          placeholder="Enter a message..."
          onInput={(ev) => ev.stopPropagation()}
          onKeyDown={(ev) => ev.stopPropagation()}
          onKeyUp={(ev) => ev.stopPropagation()}
        />
        <button type="submit" className="lk-button lk-chat-form-button" disabled={isSending}>
          Send
        </button>
      </form>
    </div>
  );
}
