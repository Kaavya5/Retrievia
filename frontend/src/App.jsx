import { useState } from 'react'
import LandingPage from './components/LandingPage'
import ChatApp from './components/ChatApp'

function App() {
  const [entered, setEntered] = useState(false)

  return (
    <div className="min-h-screen bg-pastel-background font-sans text-pastel-dark">
      {!entered ? (
        <LandingPage onEnter={() => setEntered(true)} />
      ) : (
        <ChatApp />
      )}
    </div>
  )
}

export default App
