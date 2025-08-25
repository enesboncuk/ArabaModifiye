import { useMemo, useRef, useState, useEffect } from 'react'
import './App.css'
import { 
  API_BASE, 
  recolor, 
  segment, 
  uploadImage, 
  signup, 
  login, 
  getCurrentUser,
  createProject,
  getProjects,
  getWheels,
  overlayWheel
} from './api'

interface User {
  id: number
  email: string
}

interface Project {
  id: number
  title: string
  created_at: string
  image_count: number
}

interface Wheel {
  id: number
  brand: string
  model: string
  thumb_url?: string
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [projects, setProjects] = useState<Project[]>([])
  const [currentProject, setCurrentProject] = useState<Project | null>(null)
  const [wheels, setWheels] = useState<Wheel[]>([])
  const [selectedWheel, setSelectedWheel] = useState<Wheel | null>(null)
  
  // Image states
  const [localUrl, setLocalUrl] = useState<string | null>(null)
  const [imagePath, setImagePath] = useState<string | null>(null)
  const [maskPath, setMaskPath] = useState<string | null>(null)
  const [variantPath, setVariantPath] = useState<string | null>(null)
  const [dh, setDh] = useState(0)
  const [ds, setDs] = useState(0)
  const [dv, setDv] = useState(0)
  
  // UI states
  const [showProjects, setShowProjects] = useState(false)
  const [showWheels, setShowWheels] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  
  // Form states
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [projectTitle, setProjectTitle] = useState('')
  
  const fileRef = useRef<HTMLInputElement | null>(null)

  const displayImage = useMemo(() => {
    return variantPath ? `${API_BASE}/${variantPath}` : imagePath ? `${API_BASE}/${imagePath}` : localUrl
  }, [localUrl, imagePath, variantPath])

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      setToken(savedToken)
      fetchUser(savedToken)
    }
  }, [])

  const fetchUser = async (userToken: string) => {
    try {
      const userData = await getCurrentUser(userToken)
      setUser(userData)
      fetchProjects(userToken)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      localStorage.removeItem('token')
      setToken(null)
    }
  }

  const fetchProjects = async (userToken: string) => {
    try {
      const projectsData = await getProjects(userToken)
      setProjects(projectsData)
    } catch (error) {
      console.error('Failed to fetch projects:', error)
    }
  }

  const fetchWheels = async () => {
    try {
      const wheelsData = await getWheels()
      setWheels(wheelsData)
    } catch (error) {
      console.error('Failed to fetch wheels:', error)
    }
  }

  const handleAuth = async (isSignup: boolean) => {
    setIsLoading(true)
    try {
      const result = isSignup ? await signup(email, password) : await login(email, password)
      if (result.access_token) {
        setToken(result.access_token)
        localStorage.setItem('token', result.access_token)
        await fetchUser(result.access_token)
        setEmail('')
        setPassword('')
      }
    } catch (error) {
      console.error('Auth failed:', error)
      alert('Authentication failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    setToken(null)
    setUser(null)
    setProjects([])
    setCurrentProject(null)
    localStorage.removeItem('token')
  }

  const handleCreateProject = async () => {
    if (!projectTitle.trim() || !token) return
    
    setIsLoading(true)
    try {
      const newProject = await createProject(projectTitle, token)
      setProjects([...projects, newProject])
      setCurrentProject(newProject)
      setProjectTitle('')
      setShowProjects(false)
    } catch (error) {
      console.error('Failed to create project:', error)
      alert('Failed to create project')
    } finally {
      setIsLoading(false)
    }
  }

  const handleImageUpload = async (file: File) => {
    if (!file) return
    
    setIsLoading(true)
    try {
      setVariantPath(null)
      setMaskPath(null)
      setLocalUrl(URL.createObjectURL(file))
      
      const res = await uploadImage(file, currentProject?.id, token || undefined)
      setImagePath(res.image_path)
    } catch (error) {
      console.error('Upload failed:', error)
      alert('Image upload failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSegment = async () => {
    if (!imagePath) return
    
    setIsLoading(true)
    try {
      const res = await segment(imagePath, token || undefined)
      setMaskPath(res.mask_path)
    } catch (error) {
      console.error('Segmentation failed:', error)
      alert('Segmentation failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRecolor = async () => {
    if (!imagePath || !maskPath) return
    
    setIsLoading(true)
    try {
      const res = await recolor(imagePath, maskPath, dh, ds, dv, token || undefined)
      setVariantPath(res.image_path)
    } catch (error) {
      console.error('Recoloring failed:', error)
      alert('Recoloring failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleWheelOverlay = async () => {
    if (!imagePath || !selectedWheel || !token) return
    
    // For demo purposes, we'll use placeholder points
    // In a real app, user would click 4 points on the image
    const points = [
      { x: 100, y: 100 },
      { x: 200, y: 100 },
      { x: 200, y: 200 },
      { x: 100, y: 200 }
    ]
    
    setIsLoading(true)
    try {
      const res = await overlayWheel(imagePath, selectedWheel.thumb_url || '', points, token)
      setVariantPath(res.image_path)
    } catch (error) {
      console.error('Wheel overlay failed:', error)
      alert('Wheel overlay failed')
    } finally {
      setIsLoading(false)
    }
  }

  if (!token) {
    return (
      <div className="container">
        <h1>Araba Modifiye MVP</h1>
        <div className="auth-container">
          <h2>Giriş Yap veya Kayıt Ol</h2>
          <div className="auth-form">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Şifre"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div className="auth-buttons">
              <button 
                onClick={() => handleAuth(false)}
                disabled={isLoading}
              >
                {isLoading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
              </button>
              <button 
                onClick={() => handleAuth(true)}
                disabled={isLoading}
              >
                {isLoading ? 'Kayıt olunuyor...' : 'Kayıt Ol'}
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <header className="app-header">
        <h1>Araba Modifiye MVP</h1>
        <div className="user-info">
          <span>Hoş geldin, {user?.email}</span>
          <button onClick={handleLogout}>Çıkış</button>
        </div>
      </header>

      <div className="main-content">
        <div className="sidebar">
          <div className="section">
            <h3>Projeler</h3>
            <button onClick={() => setShowProjects(!showProjects)}>
              {showProjects ? 'Gizle' : 'Göster'}
            </button>
            {showProjects && (
              <div className="projects-list">
                {projects.map(project => (
                  <div 
                    key={project.id} 
                    className={`project-item ${currentProject?.id === project.id ? 'active' : ''}`}
                    onClick={() => setCurrentProject(project)}
                  >
                    <span>{project.title}</span>
                    <small>{project.image_count} resim</small>
                  </div>
                ))}
                <div className="create-project">
                  <input
                    type="text"
                    placeholder="Proje adı"
                    value={projectTitle}
                    onChange={(e) => setProjectTitle(e.target.value)}
                  />
                  <button onClick={handleCreateProject} disabled={!projectTitle.trim()}>
                    Yeni Proje
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="section">
            <h3>Jantlar</h3>
            <button onClick={() => {
              if (wheels.length === 0) fetchWheels()
              setShowWheels(!showWheels)
            }}>
              {showWheels ? 'Gizle' : 'Göster'}
            </button>
            {showWheels && (
              <div className="wheels-list">
                {wheels.map(wheel => (
                  <div 
                    key={wheel.id} 
                    className={`wheel-item ${selectedWheel?.id === wheel.id ? 'active' : ''}`}
                    onClick={() => setSelectedWheel(wheel)}
                  >
                    <span>{wheel.brand} {wheel.model}</span>
                    {wheel.thumb_url && (
                      <img src={`${API_BASE}/${wheel.thumb_url}`} alt={wheel.model} />
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="workspace">
          <div className="controls">
            <div className="upload-section">
              <input 
                ref={fileRef} 
                type="file" 
                accept="image/*" 
                onChange={(e) => {
                  const f = e.target.files?.[0]
                  if (f) handleImageUpload(f)
                }} 
              />
              {currentProject && (
                <span className="project-info">Proje: {currentProject.title}</span>
              )}
            </div>

            <div className="action-buttons">
              <button 
                disabled={!imagePath || isLoading} 
                onClick={handleSegment}
              >
                {isLoading ? 'Segmentasyon...' : 'Segment'}
              </button>
              
              <button 
                disabled={!imagePath || !maskPath || isLoading} 
                onClick={handleRecolor}
              >
                {isLoading ? 'Renk değişimi...' : 'Renk Değiştir'}
              </button>
              
              <button 
                disabled={!imagePath || !selectedWheel || isLoading} 
                onClick={handleWheelOverlay}
              >
                {isLoading ? 'Jant ekleniyor...' : 'Jant Ekle'}
              </button>
            </div>

            <div className="sliders">
              <label>Hue (dh): {dh}
                <input 
                  type="range" 
                  min={-90} 
                  max={90} 
                  value={dh} 
                  onChange={(e) => setDh(parseInt(e.target.value))} 
                />
              </label>
              <label>Saturation (ds): {ds}
                <input 
                  type="range" 
                  min={-1} 
                  max={1} 
                  step={0.05} 
                  value={ds} 
                  onChange={(e) => setDs(parseFloat(e.target.value))} 
                />
              </label>
              <label>Value (dv): {dv}
                <input 
                  type="range" 
                  min={-1} 
                  max={1} 
                  step={0.05} 
                  value={dv} 
                  onChange={(e) => setDv(parseFloat(e.target.value))} 
                />
              </label>
            </div>
          </div>

          <div className="preview">
            {displayImage && (
              <img 
                src={displayImage} 
                style={{ maxWidth: 800, width: '100%', border: '1px solid #ddd' }} 
                alt="Preview"
              />
            )}
            {maskPath && (
              <div className="debug-info">
                <a href={`${API_BASE}/${maskPath}`} target="_blank" rel="noopener noreferrer">
                  Mask (debug)
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
