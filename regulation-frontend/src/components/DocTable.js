export default function DocTable({ rows, onDownload, onDelete }) {
  return (
    <table className="doc-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>File</th>
          <th>Exporter</th>
          <th>Destination</th>
          <th>Created</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((r) => (
          <tr key={r.id}>
            <td>{r.id}</td>
            <td>{r.file_name}</td>
            <td>{r.exporter}</td>
            <td>{r.destination}</td>
            <td>{new Date(r.created_at).toLocaleString()}</td>
            <td>
              <button onClick={() => onDownload(r.id, r.file_name)}>DL</button>
              <button onClick={() => onDelete(r.id)}>DEL</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
