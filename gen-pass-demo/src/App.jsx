import { useState } from 'react'
import './App.css'

// Load JSON files from public/
async function loadProfiles() {
  const res = await fetch("/generated_profiles.json")
  return await res.json()
}

async function loadPasswords() {
  const res = await fetch("/clean_passwords.json")
  return await res.json()
}

function App() {
  const [profiles, setProfiles] = useState(null)
  const [passwords, setPasswords] = useState(null)

  const handleLoadProfiles = async () => {
    try {
      const data = await loadProfiles()
      setProfiles(data)
    } catch (e) {
      console.error("Error loading profiles:", e)
    }
  }

  const handleLoadPasswords = async () => {
    try {
      const data = await loadPasswords()
      setPasswords(data)
    } catch (e) {
      console.error("Error loading passwords:", e)
    }
  }

  return (
    <>
      <div>
        <h1>Generate Passwords Demo</h1>

        <button onClick={handleLoadProfiles}>
          Load Profiles JSON
        </button>
        <br /><br />

        <button onClick={handleLoadPasswords}>
          Load Passwords JSON
        </button>

        <hr />

        {/* Display PROFILES */}
        {profiles && (
          <div>
            <h2>Profiles</h2>
            <pre>{JSON.stringify(profiles, null, 2)}</pre>
          </div>
        )}

        <hr />

        {/* Display PASSWORDS */}
        {passwords && (
          <div>
            <h2>Generated Passwords</h2>
            <pre>{JSON.stringify(passwords, null, 2)}</pre>
          </div>
        )}
      </div>
    </>
  )
}

export default App
