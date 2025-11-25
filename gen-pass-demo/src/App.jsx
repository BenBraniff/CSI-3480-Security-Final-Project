import { useState } from "react";
import "./App.css";
import "boxicons/css/boxicons.min.css";


async function loadProfiles() {
  await new Promise((r) => setTimeout(r, 1200)); // fake loading delay
  const res = await fetch("/generated_profiles.json");
  return await res.json();
}

async function loadPasswords() {
  await new Promise((r) => setTimeout(r, 1200)); // fake loading delay
  const res = await fetch("/clean_passwords.json");
  return await res.json();
}

function App() {
  const [profiles, setProfiles] = useState(null);
  const [passwords, setPasswords] = useState(null);

  const [loadingProfiles, setLoadingProfiles] = useState(false);
  const [loadingPasswords, setLoadingPasswords] = useState(false);

  const handleLoadProfiles = async () => {
    setLoadingProfiles(true);
    setPasswords(null); // reset password cards
    try {
      const data = await loadProfiles();
      setProfiles(data);
    } catch (err) {
      console.error("Error loading profiles:", err);
    }
    setLoadingProfiles(false);
  };

  const handleLoadPasswords = async () => {
    setLoadingPasswords(true);
    try {
      const data = await loadPasswords();
      setPasswords(data);
    } catch (err) {
      console.error("Error loading passwords:", err);
    }
    setLoadingPasswords(false);
  };

  const CARD_STYLE = {
    width: "400px",
    border: "1px solid #ccc",
    padding: "12px",
    borderRadius: "8px",
    background: "none",
    boxSizing: "border-box",
  };

  const SCROLL_CONTAINER = {
    display: "flex",
    flexDirection: "row",
    gap: "20px",
    overflowX: "auto",
    paddingBottom: "10px",
    paddingTop: "10px",
    whiteSpace: "nowrap",
    maxWidth: "1000px",
  };

  // Simple CSS spinner
  const spinner = (
    <div
      style={{
        width: "40px",
        height: "40px",
        margin: "20px auto",
        border: "5px solid #ccc",
        borderTopColor: "#333",
        borderRadius: "50%",
        animation: "spin 0.8s linear infinite",
      }}
    />
  );

  return (
    <div style={{ padding: "20px" }}>
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>

      <h1>Generate Passwords Demo</h1>

      {/* LOAD PROFILES BUTTON */}
      <button onClick={handleLoadProfiles} disabled={loadingProfiles}>
        <i className="bx bx-user" style={{ marginRight: "6px" }}></i>
        {loadingProfiles ? "Loading Profiles..." : "Load Profiles"}
      </button>

      {loadingProfiles && spinner}

      <hr />

      {/* PROFILES DISPLAY */}
      {profiles && !loadingProfiles && (
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

          {/* GENERATE PASSWORDS BUTTON */}
          <button onClick={handleLoadPasswords} disabled={loadingPasswords}>
            <i className="bx bx-brain" style={{ marginRight: "6px" }}></i>
            {loadingPasswords ? "Generating..." : "Generate Passwords"}
          </button>
        </div>
      )}

      {loadingPasswords && spinner}

      <hr />

      {/* PASSWORDS DISPLAY */}
      {passwords && !loadingPasswords && (
        <div>
          <h2>Generated Passwords</h2>
          <div style={SCROLL_CONTAINER}>
            {Object.entries(passwords).map(([studentId, pwList]) => (
              <div key={studentId} style={CARD_STYLE}>
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
