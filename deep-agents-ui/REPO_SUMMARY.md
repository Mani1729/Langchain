# Deep-Agents-UI Repository Summary

## Overview
Deep-Agents-UI is a Next.js frontend specifically designed to visualize and interact with deepagents execution flows. It provides real-time monitoring, task visualization, and sub-agent delegation tracking with a rich interactive interface for observing complex agent workflows.

## Repository Purpose
- Visualize deepagent planning and execution
- Monitor task progression and sub-agent delegation
- Provide interactive debugging of agent workflows
- Display file system operations and shell commands
- Track agent state changes in real-time

## Key Concepts

### Deepagents Visualization
- Real-time agent execution monitoring
- Task/sub-task hierarchy visualization
- Agent planning step display
- Execution result tracking

### Interactive Debugging
- View file system operations
- Monitor shell command execution
- Inspect tool call results
- Trace agent decision-making

### Workflow Monitoring
- Task dependency tracking
- Sub-agent execution status
- Resource usage monitoring
- Error detection and display

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Next.js 16, React 19.1 |
| **Language** | TypeScript 5.x |
| **Styling** | Tailwind CSS, Sass |
| **UI Components** | Radix UI, Lucide Icons |
| **Layout** | React Resizable Panels |
| **Diff Display** | Diff viewer component |
| **Notifications** | Sonner (toast notifications) |
| **LangGraph** | LangGraph SDK |
| **State Management** | React hooks, URL state |
| **Real-time** | WebSocket or Server-Sent Events |
| **Deployment** | Vercel, any Node.js host |

## High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│          Browser / Client                           │
└──────────────────┬──────────────────────────────────┘
                   │ WebSocket / SSE
┌──────────────────▼──────────────────────────────────┐
│      Next.js Application (Frontend)                 │
├──────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │  Dashboard Component                        │   │
│  │  - Task hierarchy tree                      │   │
│  │  - Real-time status updates                 │   │
│  │  - Planning step display                    │   │
│  └─────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │  Workflow Panels (Resizable)                │   │
│  │  - File Browser                             │   │
│  │  - Shell Output                             │   │
│  │  - Diff Viewer                              │   │
│  │  - Tool Results                             │   │
│  └─────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐   │
│  │  State Management                           │   │
│  │  - Agent execution state                    │   │
│  │  - Selected task/file                       │   │
│  │  - Panel layout preferences                 │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Deepagents Server   │
        │  - Agent execution   │
        │  - Task management   │
        │  - File operations   │
        └─────────────────────┘
```

## Design Patterns

### 1. **Real-Time Event Streaming**
- WebSocket or SSE connection to deepagents
- Event-driven UI updates
- Minimal polling overhead

### 2. **Hierarchical Task Visualization**
- Tree structure for task relationships
- Expandable/collapsible nodes
- Color-coded status indicators

### 3. **Resizable Panel Layout**
- React Resizable Panels for flexible layout
- User-customizable panel sizes
- Persistent layout preferences in local storage
- Responsive design on mobile

### 4. **Diff Visualization**
- Visual representation of file changes
- Side-by-side comparison
- Syntax highlighting for code changes
- Addition/deletion highlighting

### 5. **Multi-View Architecture**
- File browser view
- Shell command output view
- Diff viewer for changes
- Tool results display
- Planning steps view

## Main Features

1. **Real-Time Monitoring**: Live updates of agent execution
2. **Task Hierarchy**: Visual tree of tasks and sub-tasks
3. **File Browser**: Navigate agent-modified filesystem
4. **Shell Command Viewing**: See executed commands and results
5. **Diff Viewer**: Visualize file changes made by agent
6. **Planning Steps**: Display agent's reasoning and planning
7. **Status Indicators**: Color-coded task status (pending, running, completed, failed)
8. **Resizable Panels**: Customize workspace layout
9. **Toast Notifications**: Real-time alerts for important events
10. **Responsive Design**: Works on desktop, tablet, mobile

## File Structure

```
deep-agents-ui/
├── src/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Main dashboard
│   │   ├── api/               # API routes
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── task-tree.tsx      # Task hierarchy
│   │   ├── file-browser.tsx   # File explorer
│   │   ├── shell-output.tsx   # Command results
│   │   ├── diff-viewer.tsx    # Diff display
│   │   ├── planning-view.tsx  # Agent planning
│   │   ├── panel-layout.tsx   # Resizable panels
│   │   └── ui/                # Radix UI components
│   ├── lib/
│   │   ├── hooks/             # Custom hooks
│   │   ├── utils/             # Utilities
│   │   └── types.ts           # Type definitions
│   └── styles/                # CSS modules
├── next.config.ts             # Next.js configuration
├── tailwind.config.mjs        # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
└── package.json               # Dependencies
```

## Configuration

### Environment Variables
```env
NEXT_PUBLIC_DEEPAGENTS_API_URL=http://localhost:8000
NEXT_PUBLIC_AGENT_ID=default-agent
NEXT_PUBLIC_WS_PROTOCOL=ws  # or wss for secure
```

### Connection Setup
- WebSocket connection URL
- Agent ID to monitor
- Auto-reconnect on disconnect
- Heartbeat/ping-pong for connection health

## Integration Points

1. **Deepagents Server**: WebSocket connection for real-time updates
2. **File System API**: Fetch file contents and directory listings
3. **Shell Command API**: Retrieve command results
4. **Agent State API**: Get current agent execution state
5. **Planning API**: Fetch agent planning steps

## Key Components

### Task Tree Component
- Displays hierarchical task structure
- Expandable nodes for sub-tasks
- Status indicators (pending, running, completed, failed)
- Click to select and view details

### File Browser Component
- Navigate file system structure
- Preview file contents
- Highlight modified files
- Context menu for actions

### Shell Output Component
- Display executed commands
- Show command output
- Color-coded exit codes
- Command history

### Diff Viewer Component
- Side-by-side or unified view
- Syntax highlighting for code
- Line number display
- Addition/deletion tracking

### Planning View Component
- Display agent's reasoning steps
- Show decision rationale
- Display tool selections
- Track thought process

## Customization Points

1. Color scheme and theming via Tailwind
2. Panel layout customization
3. Component styling via CSS modules
4. Custom status indicators
5. Additional visualization panels
6. Task filtering and search

## Use Cases

- Real-time monitoring of long-running agent tasks
- Debugging complex multi-step workflows
- Observing file system operations
- Tracking sub-agent delegation
- Performance analysis of agent execution
- Demonstration of agent capabilities
- Educational visualization of agent reasoning

## Performance Considerations

- Virtual scrolling for large task hierarchies
- Lazy loading of file contents
- Debounced panel resize operations
- Connection pooling for WebSocket
- Memoization of expensive computations
- Tree pruning for historical tasks

## Monitoring & Analytics

- Agent execution time tracking
- Task success/failure rates
- File operation statistics
- Command execution metrics
- Panel interaction analytics

## Integration with Deepagents

The UI communicates with deepagents through:
- WebSocket for real-time events
- REST API for historical data
- Event streaming for task updates
- Callback hooks for state changes
- Message queue integration (optional)

## Best Practices

1. Keep WebSocket connection alive with heartbeats
2. Implement exponential backoff for reconnection
3. Cache file contents to reduce API calls
4. Use virtualization for large lists
5. Implement proper error boundaries
6. Monitor UI performance
7. Provide clear visual feedback for operations
8. Support keyboard shortcuts for power users
