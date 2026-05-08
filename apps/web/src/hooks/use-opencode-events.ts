import { useEffect, useRef } from "react";
import { mutate } from "swr";
import type {
  Event,
  PermissionRequest,
  QuestionRequest,
  Session,
  SessionStatus,
  SessionMessage,
  SessionMessageAssistant,
  SessionMessageAssistantReasoning,
  SessionMessageAssistantText,
  SessionMessageAssistantTool,
} from "@opencode-ai/sdk/v2";
import { getMessagesKey, sortSessionMessages } from "@/hooks/use-session-messages";

type RuntimeEvent =
  | Event
  | {
      id: string;
      type: "server.heartbeat" | "portal.event.error";
      properties: Record<string, unknown>;
    };

function sessionsKey(port: number) {
  return `/api/opencode/${port}/sessions`;
}

function permissionsKey(port: number) {
  return `/api/opencode/${port}/permissions`;
}

function questionsKey(port: number) {
  return `/api/opencode/${port}/questions`;
}

function gitDiffKey(port: number) {
  return `/api/opencode/${port}/git/diff`;
}

function currentProjectKey(port: number) {
  return `/api/opencode/${port}/project/current`;
}

function sessionStatusKey(port: number) {
  return `/api/opencode/${port}/session/status`;
}

function upsertById<T extends { id: string }>(items: T[] | undefined, item: T) {
  const next = [...(items ?? [])];
  const index = next.findIndex((value) => value.id === item.id);
  if (index >= 0) {
    next[index] = item;
  } else {
    next.push(item);
  }
  return next;
}

function removeById<T extends { id: string }>(
  items: T[] | undefined,
  id: string,
) {
  return (items ?? []).filter((item) => item.id !== id);
}

function sortSessions(sessions: Session[]) {
  return [...sessions].sort(
    (a: Session, b: Session) =>
      (b.time.updated ?? b.time.created) - (a.time.updated ?? a.time.created),
  );
}

function mutateSessions(port: number, updater: (items: Session[]) => Session[]) {
  void mutate<Session[]>(
    sessionsKey(port),
    (current) => updater(current ?? []),
    { revalidate: false },
  );
}

function mutatePermissions(
  port: number,
  updater: (items: PermissionRequest[]) => PermissionRequest[],
) {
  void mutate<PermissionRequest[]>(
    permissionsKey(port),
    (current) => updater(current ?? []),
    { revalidate: false },
  );
}

function mutateQuestions(
  port: number,
  updater: (items: QuestionRequest[]) => QuestionRequest[],
) {
  void mutate<QuestionRequest[]>(
    questionsKey(port),
    (current) => updater(current ?? []),
    { revalidate: false },
  );
}

function mutateSessionStatuses(
  port: number,
  updater: (items: Record<string, SessionStatus>) => Record<string, SessionStatus>,
) {
  void mutate<Record<string, SessionStatus>>(
    sessionStatusKey(port),
    (current) => updater(current ?? {}),
    { revalidate: false },
  );
}

function mutateMessages(
  port: number,
  sessionID: string,
  updater: (items: SessionMessage[]) => SessionMessage[],
) {
  void mutate<SessionMessage[]>(
    getMessagesKey(port, sessionID),
    (current) => updater(current ?? []),
    { revalidate: false },
  );
}

function revalidateMessages(port: number, sessionID: string) {
  void mutate(getMessagesKey(port, sessionID));
}

const messageRevalidationTimers = new Map<string, ReturnType<typeof setTimeout>>();

function messageRevalidationKey(port: number, sessionID: string) {
  return `${port}:${sessionID}`;
}

function revalidateMessagesSoon(port: number, sessionID: string) {
  const key = messageRevalidationKey(port, sessionID);
  if (messageRevalidationTimers.has(key)) return;

  const timer = setTimeout(() => {
    messageRevalidationTimers.delete(key);
    revalidateMessages(port, sessionID);
  }, 300);

  messageRevalidationTimers.set(key, timer);
}

function revalidateMessagesNow(port: number, sessionID: string) {
  const key = messageRevalidationKey(port, sessionID);
  const timer = messageRevalidationTimers.get(key);
  if (timer) {
    clearTimeout(timer);
    messageRevalidationTimers.delete(key);
  }

  revalidateMessages(port, sessionID);
}

function upsertMessage(messages: SessionMessage[], message: SessionMessage) {
  const next = [...messages];
  const index = next.findIndex((item) => item.id === message.id);
  if (index >= 0) {
    next[index] = message;
  } else {
    next.push(message);
  }
  return sortSessionMessages(next);
}

function replaceMessageAt(
  messages: SessionMessage[],
  index: number,
  message: SessionMessage,
) {
  const next = [...messages];
  next[index] = message;
  return next;
}

function findLastIndex<T>(items: T[], predicate: (item: T) => boolean) {
  for (let index = items.length - 1; index >= 0; index -= 1) {
    if (predicate(items[index])) return index;
  }
  return -1;
}

function activeAssistantIndex(messages: SessionMessage[]) {
  return findLastIndex(
    messages,
    (message) => message.type === "assistant" && !message.time.completed,
  );
}

function latestToolIndex(
  assistant: SessionMessageAssistant,
  callID?: string,
) {
  return findLastIndex(
    assistant.content,
    (item) => item.type === "tool" && (callID === undefined || item.id === callID),
  );
}

function latestTextIndex(assistant: SessionMessageAssistant) {
  return findLastIndex(assistant.content, (item) => item.type === "text");
}

function latestReasoningIndex(
  assistant: SessionMessageAssistant,
  reasoningID: string,
) {
  return findLastIndex(
    assistant.content,
    (item) => item.type === "reasoning" && item.id === reasoningID,
  );
}

function updateActiveAssistant(
  messages: SessionMessage[],
  updater: (assistant: SessionMessageAssistant) => SessionMessageAssistant,
) {
  const index = activeAssistantIndex(messages);
  if (index < 0) return messages;

  const assistant = messages[index];
  if (assistant.type !== "assistant") return messages;
  return replaceMessageAt(messages, index, updater(assistant));
}

function updateLatestTool(
  assistant: SessionMessageAssistant,
  callID: string,
  updater: (tool: SessionMessageAssistantTool) => SessionMessageAssistantTool,
) {
  const toolIndex = latestToolIndex(assistant, callID);
  if (toolIndex < 0) return assistant;

  const tool = assistant.content[toolIndex];
  if (tool.type !== "tool") return assistant;

  const content = [...assistant.content];
  content[toolIndex] = updater(tool);
  return { ...assistant, content };
}

function closeActiveAssistant(
  messages: SessionMessage[],
  timestamp: number,
) {
  return updateActiveAssistant(messages, (assistant) => ({
    ...assistant,
    time: {
      ...assistant.time,
      completed: timestamp,
    },
  }));
}

function appendAssistantContent(
  messages: SessionMessage[],
  item: SessionMessageAssistant["content"][number],
) {
  return updateActiveAssistant(messages, (assistant) => ({
    ...assistant,
    content: [...assistant.content, item],
  }));
}

function removeMatchingOptimisticUser(
  messages: SessionMessage[],
  text: string,
) {
  return messages.filter(
    (message) =>
      !(
        message.type === "user" &&
        message.text === text &&
        message.metadata?.portalOptimistic === true
      ),
  );
}

function revalidateInstance(port: number) {
  void mutate(sessionsKey(port));
  void mutate(sessionStatusKey(port));
  void mutate(permissionsKey(port));
  void mutate(questionsKey(port));
  void mutate(
    (key) =>
      typeof key === "string" &&
      key.startsWith(`/api/opencode/${port}/session/`) &&
      key.endsWith("/messages"),
  );
}

function applyEvent(port: number, event: RuntimeEvent) {
  switch (event.type) {
    case "server.connected":
      revalidateInstance(port);
      break;

    case "server.heartbeat":
    case "portal.event.error":
      break;

    case "session.created":
    case "session.updated":
      mutateSessions(port, (items) =>
        sortSessions(upsertById(items, event.properties.info)),
      );
      break;

    case "session.deleted":
      mutateSessions(port, (items) =>
        removeById(items, event.properties.sessionID),
      );
      mutateSessionStatuses(port, (items) => {
        const next = { ...items };
        delete next[event.properties.sessionID];
        return next;
      });
      break;

    case "session.status":
      mutateSessionStatuses(port, (items) => ({
        ...items,
        [event.properties.sessionID]: event.properties.status,
      }));
      break;

    case "session.idle":
      mutateSessionStatuses(port, (items) => ({
        ...items,
        [event.properties.sessionID]: { type: "idle" },
      }));
      revalidateMessagesNow(port, event.properties.sessionID);
      break;

    case "session.next.agent.switched":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(items, {
          id: event.id,
          type: "agent-switched",
          agent: event.properties.agent,
          time: {
            created: event.properties.timestamp,
          },
        }),
      );
      break;

    case "session.next.model.switched":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(items, {
          id: event.id,
          type: "model-switched",
          model: event.properties.model,
          time: {
            created: event.properties.timestamp,
          },
        }),
      );
      break;

    case "session.next.prompted":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(
          removeMatchingOptimisticUser(items, event.properties.prompt.text),
          {
            id: event.id,
            type: "user",
            text: event.properties.prompt.text,
            files: event.properties.prompt.files,
            agents: event.properties.prompt.agents,
            time: {
              created: event.properties.timestamp,
            },
          },
        ),
      );
      break;

    case "session.next.synthetic":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(items, {
          id: event.id,
          type: "synthetic",
          sessionID: event.properties.sessionID,
          text: event.properties.text,
          time: {
            created: event.properties.timestamp,
          },
        }),
      );
      break;

    case "session.next.shell.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(items, {
          id: event.id,
          type: "shell",
          callID: event.properties.callID,
          command: event.properties.command,
          output: "",
          time: {
            created: event.properties.timestamp,
          },
        }),
      );
      break;

    case "session.next.shell.ended":
      mutateMessages(port, event.properties.sessionID, (items) => {
        const index = findLastIndex(
          items,
          (item) =>
            item.type === "shell" && item.callID === event.properties.callID,
        );
        if (index < 0) return items;

        const shell = items[index];
        if (shell.type !== "shell") return items;
        return replaceMessageAt(items, index, {
          ...shell,
          output: event.properties.output,
          time: {
            ...shell.time,
            completed: event.properties.timestamp,
          },
        });
      });
      break;

    case "session.next.step.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(closeActiveAssistant(items, event.properties.timestamp), {
          id: event.id,
          type: "assistant",
          agent: event.properties.agent,
          model: event.properties.model,
          content: [],
          time: {
            created: event.properties.timestamp,
          },
          ...(event.properties.snapshot
            ? { snapshot: { start: event.properties.snapshot } }
            : {}),
        }),
      );
      break;

    case "session.next.step.ended":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => ({
          ...assistant,
          finish: event.properties.finish,
          cost: event.properties.cost,
          tokens: event.properties.tokens,
          time: {
            ...assistant.time,
            completed: event.properties.timestamp,
          },
          ...(event.properties.snapshot
            ? {
                snapshot: {
                  ...(assistant.snapshot ?? {}),
                  end: event.properties.snapshot,
                },
              }
            : {}),
        })),
      );
      break;

    case "session.next.step.failed":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => ({
          ...assistant,
          finish: "error",
          error: event.properties.error,
          time: {
            ...assistant.time,
            completed: event.properties.timestamp,
          },
        })),
      );
      break;

    case "session.next.text.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        appendAssistantContent(items, {
          type: "text",
          text: "",
        }),
      );
      break;

    case "session.next.text.delta":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => {
          const textIndex = latestTextIndex(assistant);
          if (textIndex < 0) return assistant;

          const text = assistant.content[textIndex];
          if (text.type !== "text") return assistant;

          const content = [...assistant.content];
          content[textIndex] = {
            ...text,
            text: `${text.text}${event.properties.delta}`,
          } satisfies SessionMessageAssistantText;
          return { ...assistant, content };
        }),
      );
      break;

    case "session.next.text.ended":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => {
          const textIndex = latestTextIndex(assistant);
          if (textIndex < 0) return assistant;

          const text = assistant.content[textIndex];
          if (text.type !== "text") return assistant;

          const content = [...assistant.content];
          content[textIndex] = {
            ...text,
            text: event.properties.text,
          } satisfies SessionMessageAssistantText;
          return { ...assistant, content };
        }),
      );
      break;

    case "session.next.reasoning.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        appendAssistantContent(items, {
          type: "reasoning",
          id: event.properties.reasoningID,
          text: "",
        }),
      );
      break;

    case "session.next.reasoning.delta":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => {
          const reasoningIndex = latestReasoningIndex(
            assistant,
            event.properties.reasoningID,
          );
          if (reasoningIndex < 0) return assistant;

          const reasoning = assistant.content[reasoningIndex];
          if (reasoning.type !== "reasoning") return assistant;

          const content = [...assistant.content];
          content[reasoningIndex] = {
            ...reasoning,
            text: `${reasoning.text}${event.properties.delta}`,
          } satisfies SessionMessageAssistantReasoning;
          return { ...assistant, content };
        }),
      );
      break;

    case "session.next.reasoning.ended":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) => {
          const reasoningIndex = latestReasoningIndex(
            assistant,
            event.properties.reasoningID,
          );
          if (reasoningIndex < 0) return assistant;

          const reasoning = assistant.content[reasoningIndex];
          if (reasoning.type !== "reasoning") return assistant;

          const content = [...assistant.content];
          content[reasoningIndex] = {
            ...reasoning,
            text: event.properties.text,
          } satisfies SessionMessageAssistantReasoning;
          return { ...assistant, content };
        }),
      );
      break;

    case "session.next.tool.input.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        appendAssistantContent(items, {
          type: "tool",
          id: event.properties.callID,
          name: event.properties.name,
          time: {
            created: event.properties.timestamp,
          },
          state: {
            status: "pending",
            input: "",
          },
        }),
      );
      break;

    case "session.next.tool.input.delta":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => {
            if (tool.state.status !== "pending") return tool;
            return {
              ...tool,
              state: {
                ...tool.state,
                input: `${tool.state.input}${event.properties.delta}`,
              },
            };
          }),
        ),
      );
      break;

    case "session.next.tool.input.ended":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => {
            if (tool.state.status !== "pending") return tool;
            return {
              ...tool,
              state: {
                ...tool.state,
                input: event.properties.text,
              },
            };
          }),
        ),
      );
      break;

    case "session.next.tool.called":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => ({
            ...tool,
            name: event.properties.tool,
            provider: event.properties.provider,
            time: {
              ...tool.time,
              ran: event.properties.timestamp,
            },
            state: {
              status: "running",
              input: event.properties.input,
              structured: {},
              content: [],
            },
          })),
        ),
      );
      break;

    case "session.next.tool.progress":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => {
            if (tool.state.status !== "running") return tool;
            return {
              ...tool,
              state: {
                ...tool.state,
                structured: event.properties.structured,
                content: [...event.properties.content],
              },
            };
          }),
        ),
      );
      break;

    case "session.next.tool.success":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => {
            const input =
              tool.state.status === "running" || tool.state.status === "completed"
                ? tool.state.input
                : {};
            return {
              ...tool,
              provider: event.properties.provider,
              time: {
                ...tool.time,
                completed: event.properties.timestamp,
              },
              state: {
                status: "completed",
                input,
                structured: event.properties.structured,
                content: [...event.properties.content],
              },
            };
          }),
        ),
      );
      break;

    case "session.next.tool.failed":
      mutateMessages(port, event.properties.sessionID, (items) =>
        updateActiveAssistant(items, (assistant) =>
          updateLatestTool(assistant, event.properties.callID, (tool) => {
            const input =
              tool.state.status === "running" || tool.state.status === "completed"
                ? tool.state.input
                : {};
            const structured =
              tool.state.status === "running" ||
              tool.state.status === "completed" ||
              tool.state.status === "error"
                ? tool.state.structured
                : {};
            const content =
              tool.state.status === "running" ||
              tool.state.status === "completed" ||
              tool.state.status === "error"
                ? tool.state.content
                : [];
            return {
              ...tool,
              provider: event.properties.provider,
              time: {
                ...tool.time,
                completed: event.properties.timestamp,
              },
              state: {
                status: "error",
                input,
                structured,
                content,
                error: event.properties.error,
              },
            };
          }),
        ),
      );
      break;

    case "session.next.retried":
      revalidateMessages(port, event.properties.sessionID);
      break;

    case "session.next.compaction.started":
      mutateMessages(port, event.properties.sessionID, (items) =>
        upsertMessage(items, {
          id: event.id,
          type: "compaction",
          reason: event.properties.reason,
          summary: "",
          time: {
            created: event.properties.timestamp,
          },
        }),
      );
      break;

    case "session.next.compaction.delta":
      mutateMessages(port, event.properties.sessionID, (items) => {
        const index = findLastIndex(
          items,
          (item) => item.type === "compaction",
        );
        if (index < 0) return items;

        const compaction = items[index];
        if (compaction.type !== "compaction") return items;
        return replaceMessageAt(items, index, {
          ...compaction,
          summary: `${compaction.summary}${event.properties.text}`,
        });
      });
      break;

    case "session.next.compaction.ended":
      mutateMessages(port, event.properties.sessionID, (items) => {
        const index = findLastIndex(
          items,
          (item) => item.type === "compaction",
        );
        if (index < 0) return items;

        const compaction = items[index];
        if (compaction.type !== "compaction") return items;
        return replaceMessageAt(items, index, {
          ...compaction,
          summary: event.properties.text,
          ...(event.properties.include
            ? { include: event.properties.include }
            : {}),
        });
      });
      break;

    case "message.updated":
    case "message.part.updated":
      revalidateMessagesNow(port, event.properties.sessionID);
      break;

    case "message.part.delta":
      revalidateMessagesSoon(port, event.properties.sessionID);
      break;

    case "message.removed":
    case "message.part.removed":
      revalidateMessagesNow(port, event.properties.sessionID);
      break;

    case "session.compacted":
      revalidateMessages(port, event.properties.sessionID);
      break;

    case "session.error":
      if (event.properties.sessionID) {
        revalidateMessagesNow(port, event.properties.sessionID);
        void mutate(sessionStatusKey(port));
      }
      break;

    case "permission.asked":
      mutatePermissions(port, (items) => upsertById(items, event.properties));
      break;

    case "permission.replied":
      mutatePermissions(port, (items) =>
        removeById(items, event.properties.requestID),
      );
      break;

    case "question.asked":
      mutateQuestions(port, (items) => upsertById(items, event.properties));
      break;

    case "question.replied":
    case "question.rejected":
      mutateQuestions(port, (items) =>
        removeById(items, event.properties.requestID),
      );
      break;

    case "session.diff":
    case "vcs.branch.updated":
      void mutate(gitDiffKey(port));
      break;

    case "project.updated":
      void mutate(currentProjectKey(port));
      break;
  }
}

function parseEvent(data: string): RuntimeEvent | null {
  try {
    return JSON.parse(data) as RuntimeEvent;
  } catch {
    return null;
  }
}

export function useOpencodeEvents(port: number | null | undefined) {
  const queueRef = useRef<RuntimeEvent[]>([]);
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (!port) return;

    const flush = () => {
      timerRef.current = null;
      const events = queueRef.current;
      queueRef.current = [];
      for (const event of events) {
        applyEvent(port, event);
      }
    };

    const enqueue = (event: RuntimeEvent) => {
      queueRef.current.push(event);
      if (timerRef.current !== null) return;
      timerRef.current = window.setTimeout(flush, 16);
    };

    const source = new EventSource(`/api/opencode/${port}/events`);

    source.onmessage = (message) => {
      const event = parseEvent(message.data);
      if (event) enqueue(event);
    };

    return () => {
      source.close();
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
        timerRef.current = null;
      }
      queueRef.current = [];
    };
  }, [port]);
}
