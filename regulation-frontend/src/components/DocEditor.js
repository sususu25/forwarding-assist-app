import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { generateDoc } from "../api/documents";
import { checkErrors } from "../api/errorCheck";
import "./DocEditor.css";

const PRESETS = {
  "SUSU25": { exporter: "SUSUSU25 CO., LTD.\n1234 Good Place, Korea", consignee: "SUSUSU25 CO., LTD.\nChicago, USA" },
  "SAMSUNG": { exporter: "SAMSUNG ELECTRONICS\nSuwon, Korea", consignee: "SAMSUNG ELECTRONICS AMERICA\nNJ, USA" }
};

export default function DocEditor() {
  const [form, setForm] = useState({
    doc_type: "CI",
    exporter: "SUSUSU25 CO., LTD.\n1234 Good Place, Korea",
    consignee: "SUSUSU25 CO., LTD.\nChicago, USA",
    port_of_loading: "BUSAN, REPUBLIC OF KOREA",
    destination: "USA",
    invoice_no: `202506-${new Date().getDate()}`,
    items: [{ name: "lithium battery", hscode: "850760", packaging: "Skid", qty: 1, weight: 0 }],
  });

  const [violations, setViolations] = useState([]);
  const [errorRows, setErrorRows] = useState([]);
  const [packagingErr, setPackagingErr] = useState(false);
  const navigate = useNavigate();

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const applyPreset = (key) => {
    const p = PRESETS[key] ?? {};
    setForm((f) => ({ ...f, ...p }));
  };

  const updateItem = (idx, key, val) => {
    const items = [...form.items];
    items[idx] = { ...items[idx], [key]: val };
    setForm({ ...form, items });
  };

  const addItem = () =>
    setForm({ ...form, items: [...form.items, { name: "", hscode: "", packaging: "", qty: 1, weight: 0 }] });

  const delItem = (idx) =>
    setForm({ ...form, items: form.items.filter((_, i) => i !== idx) });
  
  const handleSave = async () => {
    setViolations([]); // Reset violations
    try {
      // Step 1: Check for violations silently
      const checkPayload = {
        destination: form.destination,
        packaging: form.items.length > 0 ? form.items[0].packaging : "",
        items: form.items,
      };
      const resCheck = await checkErrors(checkPayload);
      const vlist = resCheck.data.violations;
      setViolations(vlist);
      mapViolationsToUI(vlist);

      // Step 2: Generate document if no violations
      await generateDoc(form);
      alert("성공적으로 저장되었습니다!");
      navigate("/docs");

    } catch (e) {
      console.error("Operation failed", e);
      const errorMsg = e.response ? JSON.stringify(e.response.data) : e.message;
      setViolations([`❌ 저장 실패: ${errorMsg}`]);
      mapViolationsToUI([]);
    }
  };

  const handleCheck = async () => {
    setViolations([]); // Reset violations
    try {
      const checkPayload = {
        destination: form.destination,
        packaging: form.items.length > 0 ? form.items[0].packaging : "",
        items: form.items,
      };
      const res = await checkErrors(checkPayload);
      const found = res.data.violations;
      setViolations(found);
      mapViolationsToUI(found);
      if (found && found.length > 0) {
        alert("규정 위반 사항이 발견되었습니다.");
      } else {
        alert("규정 위반 사항이 발견되지 않았습니다.");
        mapViolationsToUI([]);
      }
    } catch (e) {
      console.error("Check failed", e);
      const errorMsg = e.response ? JSON.stringify(e.response.data) : e.message;
      setViolations([`❌ 규정 체크 실패: ${errorMsg}`]);
      mapViolationsToUI([]);
    }
  };

  const mapViolationsToUI = (vList) => {
    const rows = new Set();
    let packErr = false;
    vList.forEach(v => {
      if (v.items) {
        v.items.forEach(name => {
          form.items.forEach((it, idx) => {
            if (it.name.toLowerCase().includes(name.toLowerCase())) rows.add(idx);
          });
        });
      }
      if (v.packaging) packErr = true;
    });
    setErrorRows([...rows]);
    setPackagingErr(packErr);
  };

  return (
    <div className="editor-wrap">
      <h2>Create {form.doc_type}</h2>
      
      <label>
        Doc Type&nbsp;
        <select value={form.doc_type} onChange={(e) => set("doc_type", e.target.value)}>
          <option>CI</option> <option>PL</option>
        </select>
      </label>

      <label>
        Preset&nbsp;
        <select onChange={(e) => applyPreset(e.target.value)}>
          <option value="">-- Select --</option>
          {Object.keys(PRESETS).map((k) => ( <option key={k} value={k}>{k}</option> ))}
        </select>
      </label>
      
      <label> Exporter <textarea value={form.exporter} onChange={e=>set("exporter",e.target.value)}/></label>
      <label> Consignee <textarea value={form.consignee} onChange={e=>set("consignee",e.target.value)}/></label>
      <label> Port of Loading <input value={form.port_of_loading} onChange={e=>set("port_of_loading",e.target.value)}/></label>
      <label> Destination <input value={form.destination} onChange={e=>set("destination",e.target.value)}/></label>
      <label> Invoice No <input value={form.invoice_no} onChange={e=>set("invoice_no",e.target.value)}/></label>
      
      <fieldset><legend>Items</legend>
        <table>
          <thead><tr><th>Description</th><th>HS Code</th><th>Packaging</th><th>Qty (PCS)</th><th>Weight (KGS)</th><th></th></tr></thead>
          <tbody>
            {form.items.map((it, idx) => (
              <tr key={idx} className={errorRows.includes(idx) ? 'error' : ''}>
                <td><input value={it.name} onChange={(e) => updateItem(idx, "name", e.target.value)} /></td>
                <td><input value={it.hscode} onChange={(e) => updateItem(idx, "hscode", e.target.value)} /></td>
                <td><input className={packagingErr ? 'error-field': ''} value={it.packaging} onChange={(e) => updateItem(idx, "packaging", e.target.value)} /></td>
                <td><input type="number" min="1" value={it.qty} onChange={(e) => updateItem(idx, "qty", +e.target.value)} /></td>
                <td><input type="number" min="0" value={it.weight} onChange={(e) => updateItem(idx, "weight", +e.target.value)} /></td>
                <td>{form.items.length > 1 && (<button onClick={() => delItem(idx)}>🗑</button>)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <button type="button" onClick={addItem} className="add-row">+ Add Row</button>
      </fieldset>

      <button className="save-btn" onClick={handleSave}>Generate PDF & Save</button>
      <button className="warn-btn" onClick={handleCheck}>⚠️ 규정 위반 체크</button>

      {violations.length > 0 && (
        <ul className="violation-box">
          {violations.map((v, idx) => {
            const text = typeof v === "string" ? v : v.message +
              (v.items ? ` (문제 항목: ${v.items.join(', ')})` : '') +
              (v.packaging ? ` (포장: ${v.packaging})` : '') +
              (v.total_weight ? ` (총중량: ${v.total_weight}kg)` : '');
            return <li key={idx}>🚨 {text}</li>;
          })}
        </ul>
      )}

      <img src="/assets/Checklist.jpg" alt="" className="bottom-img" />
    </div>
  );
}