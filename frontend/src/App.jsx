import { useState } from "react";
import "./App.css";

const scholarships = [
  { id: 1, name: "National Merit Scholarship", provider: "Government of India", amount: "₹50,000", category: "Merit", deadline: "30 Nov 2026" },
  { id: 2, name: "AI & Data Science Excellence", provider: "Tech Education Foundation", amount: "₹75,000", category: "Technology", deadline: "15 Dec 2026" },
  { id: 3, name: "Women in Technology Scholarship", provider: "Future Tech Foundation", amount: "₹1,00,000", category: "Women in STEM", deadline: "20 Dec 2026" },
  { id: 4, name: "Future Innovators Scholarship", provider: "Innovation Foundation", amount: "₹40,000", category: "Innovation", deadline: "25 Jan 2027" },
];

const studentPages = [
  "Dashboard", "Profile", "Scholarships", "My Applications",
  "Documents", "Bank Details", "Notifications",
];

const adminPages = [
  "Admin Dashboard", "Admin Students",
  "Admin Applications", "Manage Scholarships",
];

function App() {
  const [page, setPage] = useState("Home");
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [selected, setSelected] = useState(null);
  const [saved, setSaved] = useState([]);
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState({});
  const [uploading, setUploading] = useState(false);
  const [applications, setApplications] = useState([]);
  const [role, setRole] = useState("Student");

  const go = (next) => {
    setPage(next);
    setMessage("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const notify = (text) => setMessage(text);

  const visibleScholarships = scholarships.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase()) &&
    (category === "All" || s.category === category)
  );

  function submitForm(e, success) {
    e.preventDefault();
    notify(success);
  }

  function openApplication(scholarship) {
    setSelected(scholarship);
    go("Application");
  }

  function renderForm(title, fields, success) {
    return (
      <section className="form-card">
        <h1>{title}</h1>
        <p>Enter your details below.</p>
        <form onSubmit={(e) => submitForm(e, success)}>
          {fields.map((field) => (
            <label key={field}>
              {field}
              <input
                required
                type={field.toLowerCase().includes("password") ? "password" :
                  field.toLowerCase().includes("email") ? "email" :
                  field.toLowerCase().includes("date") ? "date" : "text"}
                placeholder={`Enter ${field.toLowerCase()}`}
              />
            </label>
          ))}
          <button className="primary" type="submit">Submit</button>
        </form>
        {message && <p className="success">{message}</p>}
      </section>
    );
  }

  function scholarshipCards(list) {
    return (
      <div className="scholarship-grid">
        {list.map((s) => (
          <article className="scholarship-card" key={s.id}>
            <span className="tag">{s.category}</span>
            <h3>{s.name}</h3>
            <p>{s.provider}</p>
            <h2>{s.amount}</h2>
            <p>Deadline: {s.deadline}</p>
            <div className="card-actions">
              <button onClick={() => { setSelected(s); go("Scholarship Details"); }}>View Details</button>
              <button onClick={() => setSaved((old) =>
                old.includes(s.id) ? old.filter((id) => id !== s.id) : [...old, s.id]
              )}>{saved.includes(s.id) ? "♥ Saved" : "♡ Save"}</button>
            </div>
            <button className="primary full" onClick={() => openApplication(s)}>Apply Now</button>
          </article>
        ))}
        {list.length === 0 && <p>No matching scholarships found.</p>}
      </div>
    );
  }

  function renderPage() {
    switch (page) {
      case "Home":
        return (
          <>
            <section className="hero">
              <div>
                <span className="eyebrow">AI-POWERED SCHOLARSHIP PORTAL</span>
                <h1>Find the right <span>scholarship</span> for you.</h1>
                <p>Discover opportunities, simplify applications, and track your scholarship journey in one place.</p>
                <button className="primary" onClick={() => go("Scholarships")}>Find Scholarships →</button>
                <button className="secondary" onClick={() => go("Register")}>Register Now</button>
              </div>
              <div className="hero-card">
                <div className="robot">🤖</div>
                <h3>Smart Scholarship Matching</h3>
                <p>Discover opportunities for your education and future.</p>
                <div className="progress"><span /></div>
                <small>One portal. More opportunities.</small>
              </div>
            </section>
            <section className="section">
              <h2>Everything you need to move forward</h2>
              <div className="feature-grid">
                {[
                  ["🔎", "Scholarship Search", "Find opportunities by category and course."],
                  ["🤖", "AI Document Verification", "View document verification status."],
                  ["🏦", "Bank Verification", "Submit bank details for verification."],
                  ["📊", "Application Tracking", "Follow your application progress."],
                ].map(([icon, title, desc]) => (
                  <article className="feature-card" key={title}>
                    <span>{icon}</span><h3>{title}</h3><p>{desc}</p>
                  </article>
                ))}
              </div>
            </section>
            <section className="section how">
              <h2>How it works</h2>
              <p>Register → Find Scholarship → Apply → Upload Documents → Verification → Track Application</p>
            </section>
          </>
        );

      case "Login":
        return renderForm("Welcome Back", ["Email", "Password"], "Demo login submitted. Backend authentication is not connected yet.");

      case "Register":
        return renderForm("Create Your Account", [
          "Full Name", "Email", "Mobile Number", "Password",
          "Confirm Password", "Date of Birth", "Gender", "Category", "State", "District",
        ], "Demo registration submitted. Backend registration is not connected yet.");

      case "Dashboard":
      case "Admin Dashboard":
        return (
          <section className="section">
            <span className="eyebrow">{role.toUpperCase()} PORTAL</span>
            <h1>Welcome to {page}</h1>
            <p>Track scholarship progress from one place.</p>
            <div className="stats-grid">
              {[
                ["Total Applications", applications.length],
                ["Pending", applications.length],
                ["Approved", 0],
                ["Rejected", 0],
              ].map(([name, value]) => (
                <article className="stat-card" key={name}><p>{name}</p><h2>{value}</h2></article>
              ))}
            </div>
            <h2>Recommended Scholarships</h2>
            {scholarshipCards(scholarships.slice(0, 3))}
          </section>
        );

      case "Scholarships":
        return (
          <section className="section">
            <h1>Explore Scholarships</h1>
            <p>Search opportunities for your education.</p>
            <input className="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search scholarships..." />
            <select className="search" value={category} onChange={(e) => setCategory(e.target.value)}>
              {["All", ...new Set(scholarships.map((s) => s.category))].map((c) => <option key={c}>{c}</option>)}
            </select>
            {scholarshipCards(visibleScholarships)}
          </section>
        );

      case "Scholarship Details":
        return selected ? (
          <section className="form-card">
            <span className="tag">{selected.category}</span>
            <h1>{selected.name}</h1>
            <p>Provider: {selected.provider}</p>
            <h2>{selected.amount}</h2>
            <p>Deadline: {selected.deadline}</p>
            <h3>Basic eligibility</h3>
            <p>Eligibility must be confirmed with the official scholarship provider.</p>
            <button className="primary" onClick={() => openApplication(selected)}>Apply Now</button>
          </section>
        ) : <p>Select a scholarship to view details.</p>;

      case "Application":
        return (
          <section className="form-card">
            <h1>Scholarship Application</h1>
            <p>{selected?.name || "Complete your application details."}</p>
            <form onSubmit={(e) => {
              e.preventDefault();
              setApplications((old) => [...old, {
                id: Date.now(), name: selected?.name || "Scholarship Application",
                date: new Date().toLocaleDateString(), status: "Pending",
              }]);
              notify("Demo application saved in this session.");
            }}>
              {["Course", "College", "Year of Study", "Marks / CGPA", "Category", "Annual Family Income", "Address", "State", "District"].map((f) => (
                <label key={f}>{f}<input required placeholder={`Enter ${f}`} /></label>
              ))}
              <button className="primary">Submit Application</button>
            </form>
            {message && <p className="success">{message}</p>}
          </section>
        );

      case "Documents":
        return (
          <section className="form-card">
            <h1>Document Upload & AI Verification</h1>
            <p>Select the required documents. PDF, PNG, or JPG files only; maximum 5 MB per file.</p>

            {[
              "10th Certificate",
              "12th Certificate",
              "Aadhaar",
              "Income Certificate",
              "Community Certificate",
            ].map((name) => (
              <label className="upload-row" key={name}>
                {name}
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={(e) => {
                    const file = e.target.files[0];

                    if (!file) {
                      setFiles((old) => {
                        const updated = { ...old };
                        delete updated[name];
                        return updated;
                      });
                      return;
                    }

                    const allowedTypes = [
                      "application/pdf",
                      "image/png",
                      "image/jpeg",
                    ];

                    if (!allowedTypes.includes(file.type)) {
                      notify("Please select a PDF, PNG, or JPG file.");
                      e.target.value = "";
                      return;
                    }

                    if (file.size > 5 * 1024 * 1024) {
                      notify("Each file must be 5 MB or smaller.");
                      e.target.value = "";
                      return;
                    }

                    setFiles((old) => ({ ...old, [name]: file }));
                    notify("");
                  }}
                />

                {files[name] && (
                  <small>Selected: {files[name].name}</small>
                )}
              </label>
            ))}

            <button
              className="primary"
              disabled={uploading}
              onClick={() => {
                const requiredDocs = [
                  "10th Certificate",
                  "12th Certificate",
                  "Aadhaar",
                  "Income Certificate",
                  "Community Certificate",
                ];

                const missingDocs = requiredDocs.filter(
                  (name) => !files[name]
                );

                if (missingDocs.length > 0) {
                  notify(
                    "Please upload all required documents: " +
                      missingDocs.join(", ")
                  );
                  return;
                }

                notify(
                  "Documents selected and validated. Actual upload and AI verification require the backend API."
                );
              }}
            >
              {uploading ? "Uploading..." : "Submit for Verification"}
            </button>

            {message && <p className="success">{message}</p>}

            <p className="status pending">
              Awaiting backend upload and AI verification.
            </p>
          </section>
        );
      
      case "Bank Details":
        return (
          <section className="form-card">
            <h1>Bank Details</h1>
            {renderForm("Submit Bank Details", ["Account Holder Name", "Account Number", "Confirm Account Number", "Bank Name", "IFSC Code", "Branch"], "Demo bank form submitted. Real bank verification is not connected.")}
          </section>
        );

      case "My Applications":
        return (
          <section className="section">
            <h1>My Applications</h1>
            {applications.length === 0 ? <p>No applications submitted in this session yet.</p> : (
              <div className="scholarship-grid">
                {applications.map((a) => <article className="scholarship-card" key={a.id}>
                  <h3>{a.name}</h3><p>Applied: {a.date}</p><span className="status pending">{a.status}</span>
                  <p>Documents → AI Verification → Bank Verification → Review → Decision</p>
                </article>)}
              </div>
            )}
          </section>
        );

      case "Profile":
        return renderForm("Student Profile", ["Full Name", "Email", "Mobile Number", "Course", "College", "Year of Study", "Category", "Annual Family Income", "State", "District"], "Demo profile form submitted.");

      case "Notifications":
        return <section className="section"><h1>Notifications</h1>{[
          "Document verification status will appear here.",
          "Bank verification status will appear here.",
          "Application status updates will appear here.",
        ].map((n) => <article className="feature-card" key={n}>{n}</article>)}</section>;

      case "Admin Students":
        return <section className="section"><h1>Students</h1><p>Student records will appear here when connected to the backend.</p></section>;

      case "Admin Applications":
        return <section className="section"><h1>Manage Applications</h1><p>Application review and status updates will appear here.</p></section>;

      case "Manage Scholarships":
        return <section className="section"><h1>Manage Scholarships</h1>{scholarshipCards(scholarships)}<p>Adding and editing persistent scholarship records requires the backend API.</p></section>;

      default:
        return <section className="section"><h1>{page}</h1><p>Page ready for further development.</p></section>;
    }
  }

  const navPages = role === "Admin" ? adminPages : studentPages;

  return (
    <div className="app">
      <header className="navbar">
        <button className="brand" onClick={() => go("Home")}>🎓 <span>ScholarAI</span></button>
        <nav>
          <button onClick={() => go("Home")}>Home</button>
          <button onClick={() => go("Scholarships")}>Scholarships</button>
          <button onClick={() => go("Dashboard")}>Dashboard</button>
          <button onClick={() => go("My Applications")}>Applications</button>
          <button onClick={() => go("Documents")}>Documents</button>
          <button onClick={() => go("Notifications")}>Notifications</button>
        </nav>
        <div className="nav-actions">
          <select aria-label="Demo role" value={role} onChange={(e) => setRole(e.target.value)}>
            <option>Student</option><option>Admin</option>
          </select>
          <button className="primary" onClick={() => go("Login")}>Login</button>
          <button className="secondary" onClick={() => go("Register")}>Register</button>
        </div>
      </header>
      <main>{renderPage()}</main>
      <footer><strong>ScholarAI</strong><p>AI-Powered Scholarship Portal </p></footer>
    </div>
  );
}

export default App;