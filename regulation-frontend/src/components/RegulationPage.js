import { useState, useEffect, useRef } from "react";
import { getRegulationInfo } from "../api/regulation";
import "./RegPage.css";

const COUNTRIES = ["USA", "CHINA", "JAPAN", "VIETNAM", "EU"];
const CARGO_TYPES = ["general", "battery", "chemicals", "machinery", "food"];

export default function RegulationPage() {
  const [country, setCountry] = useState("USA");
  const [cargo, setCargo] = useState("general");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [countryOpen, setCountryOpen] = useState(false);
  const [cargoOpen, setCargoOpen] = useState(false);
  const countryRef = useRef(null);
  const cargoRef = useRef(null);

  const handleSearch = async () => {
    if (!country || !cargo) {
      setError("Please enter both country and cargo type.");
      setResult(null);
      return;
    }
    setError("");
    try {
      const res = await getRegulationInfo({ country, cargo_type: cargo });
      setResult(res.data);
    } catch (e) {
      console.error(e);
      setError("No data found or server error.");
      setResult(null);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  // 외부 클릭 감지
  useEffect(() => {
    function handleClickOutside(event) {
      if (countryRef.current && !countryRef.current.contains(event.target)) {
        setCountryOpen(false);
      }
      if (cargoRef.current && !cargoRef.current.contains(event.target)) {
        setCargoOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="reg-wrap">
      <h2>Regulation Lookup</h2>

      <div className="inputs">
        {/* Country Dropdown */}
        <div className="dropdown-container" ref={countryRef}>
          <input
            value={country}
            onChange={(e) => setCountry(e.target.value.toUpperCase())}
            onFocus={() => setCountryOpen(true)}
            placeholder="Country"
          />
          {countryOpen && (
            <div className="dropdown-list">
              {COUNTRIES.map(c => (
                <div key={c} className="dropdown-item" onClick={() => { setCountry(c); setCountryOpen(false); }}>
                  {c}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Cargo Dropdown */}
        <div className="dropdown-container" ref={cargoRef}>
          <input
            value={cargo}
            onChange={(e) => setCargo(e.target.value.toLowerCase())}
            onFocus={() => setCargoOpen(true)}
            placeholder="Cargo Type"
          />
          {cargoOpen && (
            <div className="dropdown-list">
              {CARGO_TYPES.map(t => (
                <div key={t} className="dropdown-item" onClick={() => { setCargo(t); setCargoOpen(false); }}>
                  {t}
                </div>
              ))}
            </div>
          )}
        </div>
        
        <button onClick={handleSearch}>Search</button>
      </div>

      {error && <p className="err">{error}</p>}
      {result && (
        <div className="card">
          <p><b>Country:</b> {result.country}</p>
          <p><b>Cargo:</b> {result.cargo_type}</p>
          <p><b>Docs:</b> {result.required_documents?.join(", ")}</p>
          <p><b>Packaging:</b> {result.packaging_requirement}</p>
          <p><b>CO:</b> {result.co_required ? "Yes" : "No"}</p>
          <p><b>Notes:</b> {result.notes}</p>
        </div>
      )}

      <img src="/assets/6181711.jpg" className="bottom-img" alt="" />
    </div>
  );
}
