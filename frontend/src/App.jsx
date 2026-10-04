import './App.css'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">
          <span>🎓</span> ScholarAI
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#scholarships">Scholarships</a>
          <a href="#about">About</a>
          <button>Login</button>
        </div>
      </nav>

      <main id="home" className="hero-section">
        <div className="hero-content">
          <p className="tagline">AI-POWERED SCHOLARSHIP PORTAL</p>

          <h1>
            Find the right
            <span> scholarship </span>
            for you.
          </h1>

          <p className="description">
            Discover scholarships that match your education, skills,
            interests and eligibility — all in one place.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn">
              Find Scholarships →
            </button>

            <button className="secondary-btn">
              Check Eligibility
            </button>
          </div>
        </div>

        <div className="hero-card">
          <div className="card-icon">🤖</div>
          <h2>Smart Matching</h2>
          <p>
            Our AI helps you discover opportunities that fit your profile.
          </p>

          <div className="match">
            <span>Scholarship Match</span>
            <strong>92%</strong>
          </div>

          <div className="progress">
            <div></div>
          </div>
        </div>
      </main>

      <section id="scholarships" className="features">
        <h2>Everything you need to find your opportunity</h2>

        <div className="feature-grid">
          <div className="feature-card">
            <span>🔍</span>
            <h3>Smart Search</h3>
            <p>
              Search scholarships based on your course, location and interests.
            </p>
          </div>

          <div className="feature-card">
            <span>🤖</span>
            <h3>AI Matching</h3>
            <p>
              Get personalized scholarship recommendations based on your profile.
            </p>
          </div>

          <div className="feature-card">
            <span>✓</span>
            <h3>Eligibility Check</h3>
            <p>
              Quickly understand whether you meet the requirements.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default App