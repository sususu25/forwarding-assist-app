import { useEffect, useState } from "react";
import { listDocs, downloadDoc, deleteDoc } from "./api/documents";
import { Link } from "react-router-dom";

export default function DocumentsPage(){
  const [docs,setDocs]=useState([]); const [loading,setLoad]=useState(false);
  const refresh=()=>{ setLoad(true); listDocs().then(r=>setDocs(r.data)).finally(()=>setLoad(false)); };
  useEffect(refresh,[]);
  const dl=(id,n)=>downloadDoc(id).then(res=>{
    const url=URL.createObjectURL(res.data); const a=document.createElement("a");
    a.href=url; a.download=n; a.click(); URL.revokeObjectURL(url);
  });
  return(
    <>
      <h1>Documents</h1>
      <Link to="/docs/create" style={{marginBottom:12,display:"inline-block"}}>➕ New Doc</Link>
      {loading? <p>Loading…</p> : docs.length===0 ? <p>No documents</p> : (
        <table border="1" cellPadding="6" width="100%">
          <thead><tr>
            <th>ID</th><th>File</th><th>Exporter</th><th>Destination</th><th>Created</th><th>Action</th>
          </tr></thead>
          <tbody>{docs.map(d=>(
            <tr key={d.id}>
              <td>{d.id}</td><td>{d.file_name}</td><td>{d.exporter}</td>
              <td>{d.destination}</td><td>{new Date(d.created_at).toLocaleString()}</td>
              <td>
                <button onClick={()=>dl(d.id,d.file_name)}>Download</button>
                <button onClick={()=>deleteDoc(d.id).then(refresh)} style={{marginLeft:4}}>Delete</button>
              </td>
            </tr>
          ))}</tbody>
        </table>
      )}
    </>
  );
}
