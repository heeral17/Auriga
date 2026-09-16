import { useMemo, useState } from "react";
import {
  AlertCircle, ArrowUp, CheckCircle2, Clock3, Search, ShieldAlert,
  UserRound, X, ChevronRight
} from "lucide-react";

type Priority = "Normal" | "High" | "Urgent";
type Status = "Open" | "In Progress" | "Resolved";

type Ticket = {
  id: number;
  customer: string;
  title: string;
  description: string;-
  priority: Priority;
  originalPriority: Priority;
  assignee: string;
  timeLeft: number; // minutes; negative = overdue
  status: Status;
  escalated: boolean;
};

const tickets: Ticket[] = [
  {
    id: 101, customer: "Acme Corporation", title: "Laptop won't boot",
    description: "Executive laptop fails to start before a client demo.",
    priority: "Urgent", originalPriority: "Urgent", assignee: "Priya",
    timeLeft: -18, status: "Open", escalated: false
  },
  {
    id: 102, customer: "GreenField Inc.", title: "Email service is not syncing",
    description: "Mailbox stopped syncing on the employee's primary device.",
    priority: "High", originalPriority: "Normal", assignee: "Priya",
    timeLeft: -7, status: "Open", escalated: true
  },
  {
    id: 103, customer: "TechNova Solutions", title: "VPN connection unavailable",
    description: "Remote employee cannot connect to the company VPN.",
    priority: "Urgent", originalPriority: "Urgent", assignee: "Rahul",
    timeLeft: 31, status: "In Progress", escalated: false
  },
  {
    id: 104, customer: "Sarah Williams", title: "Email service is not syncing",
    description: "Email is delayed across the user's desktop and mobile device.",
    priority: "Urgent", originalPriority: "Urgent", assignee: "Priya",
    timeLeft: 47, status: "Open", escalated: false
  },
  {
    id: 105, customer: "BluePeak Ltd.", title: "Cannot access shared drive",
    description: "The finance team cannot open the shared department drive.",
    priority: "High", originalPriority: "High", assignee: "Rahul",
    timeLeft: 74, status: "Open", escalated: false
  },
  {
    id: 106, customer: "John Smith", title: "Request for larger monitor",
    description: "Request for a larger monitor for spreadsheet-heavy work.",
    priority: "Normal", originalPriority: "Normal", assignee: "Priya",
    timeLeft: 510, status: "Open", escalated: false
  },
  {
    id: 107, customer: "Mira Patel", title: "Keyboard replacement",
    description: "Several keys on the current keyboard no longer work.",
    priority: "Normal", originalPriority: "Normal", assignee: "Priya",
    timeLeft: 920, status: "Open", escalated: false
  },
  {
    id: 108, customer: "Northstar Media", title: "Password reset request",
    description: "User needs a standard password reset.",
    priority: "Normal", originalPriority: "Normal", assignee: "Rahul",
    timeLeft: 1200, status: "Open", escalated: false
  }
];

const priorityRank: Record<Priority, number> = { Urgent: 0, High: 1, Normal: 2 };

function slaState(minutes: number) {
  if (minutes <= 0) return "Breached";
  if (minutes <= 30) return "At risk";
  return "On track";
}

function formatTime(minutes: number) {
  if (minutes <= 0) return `${Math.abs(minutes)} min overdue`;
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m ? `${h}h ${m}m` : `${h}h`;
}

function App() {
  const [query, setQuery] = useState("");
  const [timeFilter, setTimeFilter] = useState("All");
  const [priorityFilter, setPriorityFilter] = useState<Priority | "All">("All");
  const [statusFilter, setStatusFilter] = useState<Status | "All">("All");
  const [selected, setSelected] = useState<Ticket | null>(null);

  const filtered = useMemo(() => {
    return tickets
      .filter(t => {
        const q = query.toLowerCase();
        const matchesQuery = !q || `${t.customer} ${t.title} ${t.description}`.toLowerCase().includes(q);
        const matchesPriority = priorityFilter === "All" || t.priority === priorityFilter;
        const matchesStatus = statusFilter === "All" || t.status === statusFilter;

        const matchesTime =
          timeFilter === "All" ||
          (timeFilter === "Overdue" && t.timeLeft <= 0) ||
          (timeFilter === "<15 min" && t.timeLeft > 0 && t.timeLeft < 15) ||
          (timeFilter === "15–30 min" && t.timeLeft >= 15 && t.timeLeft <= 30) ||
          (timeFilter === "30–60 min" && t.timeLeft > 30 && t.timeLeft <= 60) ||
          (timeFilter === "1–2 hrs" && t.timeLeft > 60 && t.timeLeft <= 120) ||
          (timeFilter === ">2 hrs" && t.timeLeft > 120);

        return matchesQuery && matchesPriority && matchesStatus && matchesTime;
      })
      // Core rule: breached tickets first; otherwise nearest SLA deadline first.
      .sort((a, b) => {
        const aBucket = a.timeLeft <= 0 ? 0 : 1;
        const bBucket = b.timeLeft <= 0 ? 0 : 1;
        return aBucket - bBucket || a.timeLeft - b.timeLeft ||
          priorityRank[a.priority] - priorityRank[b.priority] || a.id - b.id;
      });
  }, [query, timeFilter, priorityFilter, statusFilter]);

  const overdue = tickets.filter(t => t.timeLeft <= 0).length;
  const urgent = tickets.filter(t => t.priority === "Urgent").length;
  const atRisk = tickets.filter(t => t.timeLeft > 0 && t.timeLeft <= 30).length;
  const inProgress = tickets.filter(t => t.status === "In Progress").length;

  return (
    <div className="min-h-screen">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <div className="flex items-center gap-2 text-xl font-bold tracking-tight">
              <div className="rounded-lg bg-slate-900 p-2 text-white"><ShieldAlert size={18}/></div>
              HelpDesk
            </div>
            <p className="mt-1 text-sm text-slate-500">Emergency response queue · SLA-first</p>
          </div>
          <div className="flex items-center gap-2 rounded-full border bg-slate-50 px-4 py-2 text-sm">
            <UserRound size={16} />
            Priya
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-7">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Who needs help next?</h1>
          <p className="mt-1 text-sm text-slate-500">
            Breached SLAs jump to the front. Within the queue, the nearest deadline comes first.
          </p>
        </div>

        <section className="mb-6 grid grid-cols-2 gap-3 md:grid-cols-4">
          <Stat icon={<AlertCircle size={18}/>} label="Urgent" value={urgent} />
          <Stat icon={<ShieldAlert size={18}/>} label="Overdue" value={overdue} danger />
          <Stat icon={<Clock3 size={18}/>} label="At risk" value={atRisk} />
          <Stat icon={<CheckCircle2 size={18}/>} label="In progress" value={inProgress} />
        </section>

        <section className="mb-6 rounded-xl border bg-white p-4 shadow-sm">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-2.5 text-slate-400" size={18}/>
              <input
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search customer or problem..."
                className="w-full rounded-lg border px-10 py-2 text-sm outline-none focus:border-slate-400"
              />
            </div>
            <Select value={timeFilter} onChange={setTimeFilter}
              options={["All", "Overdue", "<15 min", "15–30 min", "30–60 min", "1–2 hrs", ">2 hrs"]} />
            <Select value={priorityFilter} onChange={v => setPriorityFilter(v as Priority | "All")}
              options={["All", "Normal", "High", "Urgent"]} />
            <Select value={statusFilter} onChange={v => setStatusFilter(v as Status | "All")}
              options={["All", "Open", "In Progress", "Resolved"]} />
          </div>
        </section>

        <section className="overflow-hidden rounded-xl border bg-white shadow-sm">
          <div className="flex items-center justify-between border-b px-5 py-4">
            <div>
              <h2 className="font-semibold">Emergency Queue</h2>
              <p className="text-xs text-slate-500">{filtered.length} tickets · sorted automatically</p>
            </div>
            <div className="text-xs text-slate-500">Automation: SLA escalation enabled</div>
          </div>

          <div>
            {filtered.map((ticket, index) => {
              const state = slaState(ticket.timeLeft);
              return (
                <button
                  key={ticket.id}
                  onClick={() => setSelected(ticket)}
                  className="group flex w-full items-center gap-4 border-b px-5 py-4 text-left transition hover:bg-slate-50"
                >
                  <div className="w-7 text-center text-sm font-semibold text-slate-400">#{index + 1}</div>

                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-semibold text-slate-900">{ticket.customer}</span>
                      <PriorityBadge priority={ticket.priority}/>
                      {ticket.escalated && (
                        <span className="inline-flex items-center gap-1 rounded-full bg-orange-50 px-2 py-1 text-[11px] font-semibold text-orange-700">
                          <ArrowUp size={12}/> Escalated
                        </span>
                      )}
                    </div>
                    <div className="mt-1 text-sm text-slate-700">{ticket.title}</div>
                    <div className="mt-1 max-w-2xl truncate text-xs text-slate-500">{ticket.description}</div>
                  </div>

                  <div className="hidden w-40 md:block">
                    <div className="text-xs text-slate-400">SLA</div>
                    <div className={`mt-1 text-sm font-semibold ${
                      state === "Breached" ? "text-red-600" : state === "At risk" ? "text-orange-600" : "text-slate-700"
                    }`}>{state}</div>
                    <div className="text-xs text-slate-500">{formatTime(ticket.timeLeft)}</div>
                  </div>

                  <div className="hidden w-28 lg:block">
                    <div className="text-xs text-slate-400">Assigned to</div>
                    <div className="mt-1 text-sm font-medium">{ticket.assignee}</div>
                  </div>

                  <ChevronRight size={18} className="text-slate-300 transition group-hover:text-slate-600"/>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="px-6 py-16 text-center text-sm text-slate-500">No tickets match these filters.</div>
            )}
          </div>
        </section>

        <div className="mt-4 flex flex-wrap gap-4 text-xs text-slate-500">
          <span>Priority levels: Normal → High → Urgent</span>
          <span>•</span>
          <span>Escalation: max one level per automation run</span>
          <span>•</span>
          <span>No manual escalation control in Part 1</span>
        </div>
      </main>

      {selected && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4" onClick={() => setSelected(null)}>
          <div className="w-full max-w-xl rounded-2xl bg-white p-6 shadow-xl" onClick={e => e.stopPropagation()}>
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Ticket #{selected.id}</div>
                <h3 className="mt-1 text-xl font-bold">{selected.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{selected.customer}</p>
              </div>
              <button className="rounded-lg p-2 hover:bg-slate-100" onClick={() => setSelected(null)}><X size={18}/></button>
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3">
              <Info label="Priority"><PriorityBadge priority={selected.priority}/></Info>
              <Info label="SLA status"><span className={selected.timeLeft <= 0 ? "font-semibold text-red-600" : "font-semibold"}>{slaState(selected.timeLeft)}</span></Info>
              <Info label="Time remaining"><span className="font-semibold">{formatTime(selected.timeLeft)}</span></Info>
              <Info label="Assignee"><span className="font-semibold">{selected.assignee}</span></Info>
            </div>
            <div className="mt-5 rounded-xl bg-slate-50 p-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">Problem</div>
              <p className="mt-2 text-sm leading-6 text-slate-700">{selected.description}</p>
            </div>
            {selected.escalated && (
              <div className="mt-4 rounded-xl border border-orange-200 bg-orange-50 p-4 text-sm text-orange-800">
                <div className="flex items-center gap-2 font-semibold"><ArrowUp size={16}/> Automatically escalated</div>
                <p className="mt-1">Original priority: {selected.originalPriority}. Current priority: {selected.priority}. One level was added by the SLA automation.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ icon, label, value, danger = false }: { icon: React.ReactNode; label: string; value: number; danger?: boolean }) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-slate-400">{icon}</span>
        <span className={`text-2xl font-bold ${danger ? "text-red-600" : ""}`}>{value}</span>
      </div>
      <div className="mt-2 text-sm text-slate-500">{label}</div>
    </div>
  );
}

function Select({ value, onChange, options }: { value: string; onChange: (v: string) => void; options: string[] }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)}
      className="rounded-lg border bg-white px-3 py-2 text-sm outline-none focus:border-slate-400">
      {options.map(o => <option key={o}>{o}</option>)}
    </select>
  );
}

function PriorityBadge({ priority }: { priority: Priority }) {
  const classes = priority === "Urgent"
    ? "bg-red-50 text-red-700"
    : priority === "High"
      ? "bg-orange-50 text-orange-700"
      : "bg-slate-100 text-slate-600";
  return <span className={`rounded-full px-2 py-1 text-[11px] font-semibold ${classes}`}>{priority}</span>;
}

function Info({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border p-3">
      <div className="text-xs text-slate-400">{label}</div>
      <div className="mt-1 text-sm">{children}</div>
    </div>
  );
}