import { useState } from "react";
import "./App.css";

async function loadProfiles() {
  const res = await fetch("/generated_profiles.json");
  return await res.json();
}

async function loadPasswords() {
  const res = await fetch("/clean_passwords.json");
  return await res.json();
}

function App() {
  const [profiles, setProfiles] = useState(null);
  const [passwords, setPasswords] = useState(null);

  const handleLoadProfiles = async () => {
    try {
      const data = await loadProfiles();
      setProfiles(data);
    } catch (err) {
      console.error("Error loading profiles:", err);
    }
  };

  const handleLoadPasswords = async () => {
    try {
      const data = await loadPasswords();
      setPasswords(data);
    } catch (err) {
      console.error("Error loading passwords:", err);
    }
  };

  // Shared card width so everything aligns
  const CARD_STYLE = {
    width: "400px",
    // minWidth: "260px",
    border: "1px solid #ccc",
    padding: "12px",
    borderRadius: "8px",
    background: "none",
    boxSizing: "border-box",
  };

  const PASSWORD_CARD_STYLE = {
    ...CARD_STYLE,
  };

  const SCROLL_CONTAINER = {
    display: "flex",
    flexDirection: "row",
    gap: "20px",
    overflowX: "auto",
    paddingBottom: "10px",
    paddingTop: "10px",
    whiteSpace: "nowrap",
    maxWidth: "1000px"
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Generate Passwords Demo</h1>
      <button onClick={handleLoadProfiles}>Load Profiles</button>
      <br />

      <hr />
      {/* ==========================
          PROFILES DISPLAY
      ========================== */}
      {profiles && (
        <div>
          <h2>Profiles</h2>

          <div style={SCROLL_CONTAINER}>
            {profiles.map((p, idx) => (
              <div key={idx} style={CARD_STYLE}>
                <h3>{p.name}</h3>

                <p>
                  <b>ID:</b> {p.student_id}
                </p>
                <p>
                  <b>Age:</b> {p.age}
                </p>
                <p>
                  <b>School:</b> {p.school}
                </p>
                <p>
                  <b>Major:</b> {p.major}
                </p>
                <p>
                  <b>Graduation:</b> {p.graduation_year}
                </p>
                <p>
                  <b>GPA:</b> {p.gpa}
                </p>
                <p>
                  <b>Email:</b> {p.email}
                </p>
                <p>
                  <b>Location:</b> {p.city}, {p.state}
                </p>

                <p>
                  <b>Interests:</b>
                </p>
                <ul>
                  {p.interests.map((i, iidx) => (
                    <li key={iidx}>{i}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <button onClick={handleLoadPasswords}>Generate Passwords</button>
        </div>
      )}
      <hr />
      {/* ==========================
          PASSWORDS DISPLAY
      ========================== */}
      {passwords && (
        <div>
          <h2>Generated Passwords</h2>

          <div style={SCROLL_CONTAINER}>
            {Object.entries(passwords).map(([studentId, pwList]) => (
              <div key={studentId} style={PASSWORD_CARD_STYLE}>
                <h3>{studentId}</h3>
                <ul>
                  {pwList.map((pw, idx) => (
                    <li key={idx}>{pw}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
