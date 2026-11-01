import "./dashboard.css";

type Usage = { id: string; name: string; requests: number; status: "ok" | "over" };

export function UsageDashboard({ data, loading }: { data?: Usage[]; loading: boolean }) {
  const rows = data ?? [];
  const total = rows.reduce((sum, row) => sum + row.requests, 0);

  return (
    <main className="dashboard">
      <h1>Usage</h1>
      <p className="kpi">{total.toLocaleString()} requests this month</p>
      <table className="usage-table">
        <thead>
          <tr>
            <th>Project</th>
            <th className="num">Requests</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{row.name}</td>
              <td className="num">{row.requests.toLocaleString()}</td>
              <td><span className={`dot dot--${row.status}`} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
