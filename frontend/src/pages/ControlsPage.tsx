import { useState, useEffect, useCallback } from 'react'
import { 
  Shield,
  ChevronRight, 
  Search, 
  BookOpen,
  CheckCircle,
  Lock,
  Server,
  FileText,
  Eye,
  UserCheck,
  AlertTriangle,
  HelpCircle,
} from 'lucide-react'
import { Button, Card, CardHeader, CardTitle, CardContent, Badge } from '../components/ui'
import { api } from '../lib/axios'

interface Control {
  id: string
  control_id: string
  framework: string
  category: string
  title: string
  description: string
  check_type: string
  required_file_types: string
}

interface ControlCategory {
  name: string
  count: number
  controls: string[]
}

interface ControlSummary {
  total: number
  full_scan_count?: number
  by_category: Record<string, number>
  by_check_type: Record<string, number>
  summary?: {
    categories?: Record<string, number>
  }
}

const categoryIcons: Record<string, React.ReactNode> = {
  'Control Environment': <Shield className="h-5 w-5" />,
  'Communication and Information': <FileText className="h-5 w-5" />,
  'Risk Assessment': <AlertTriangle className="h-5 w-5" />,
  'Monitoring Activities': <Eye className="h-5 w-5" />,
  'Control Activities': <CheckCircle className="h-5 w-5" />,
  'Logical and Physical Access': <Lock className="h-5 w-5" />,
  'System Operations': <Server className="h-5 w-5" />,
  'Change Management': <FileText className="h-5 w-5" />,
  'Risk Mitigation': <AlertTriangle className="h-5 w-5" />,
  'Availability': <Server className="h-5 w-5" />,
  'Processing Integrity': <CheckCircle className="h-5 w-5" />,
  'Confidentiality': <Lock className="h-5 w-5" />,
  'Privacy': <UserCheck className="h-5 w-5" />,
}

const categoryColors: Record<string, string> = {
  'Control Environment': 'bg-blue-100 text-blue-700',
  'Communication and Information': 'bg-purple-100 text-purple-700',
  'Risk Assessment': 'bg-orange-100 text-orange-700',
  'Monitoring Activities': 'bg-green-100 text-green-700',
  'Control Activities': 'bg-teal-100 text-teal-700',
  'Logical and Physical Access': 'bg-indigo-100 text-indigo-700',
  'System Operations': 'bg-cyan-100 text-cyan-700',
  'Change Management': 'bg-pink-100 text-pink-700',
  'Risk Mitigation': 'bg-red-100 text-red-700',
  'Availability': 'bg-emerald-100 text-emerald-700',
  'Processing Integrity': 'bg-lime-100 text-lime-700',
  'Confidentiality': 'bg-violet-100 text-violet-700',
  'Privacy': 'bg-amber-100 text-amber-700',
}

export default function ControlsPage() {
  const [controls, setControls] = useState<Control[]>([])
  const [categories, setCategories] = useState<ControlCategory[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [scanType, setScanType] = useState<'quick' | 'full'>('full')
  const [isLoading, setIsLoading] = useState(true)
  const [summary, setSummary] = useState<ControlSummary | null>(null)
  const [expandedControl, setExpandedControl] = useState<string | null>(null)

  const loadControls = useCallback(async () => {
    try {
      setIsLoading(true)
      const response = await api.get(`/controls?scan_type=${scanType}`)
      setControls(response.data.controls)
    } catch (error) {
      console.error('Failed to load controls:', error)
    } finally {
      setIsLoading(false)
    }
  }, [scanType])

  const loadCategories = useCallback(async () => {
    try {
      const response = await api.get('/controls/categories')
      setCategories(response.data.categories)
    } catch (error) {
      console.error('Failed to load categories:', error)
    }
  }, [])

  const loadSummary = useCallback(async () => {
    try {
      const response = await api.get('/controls/summary')
      setSummary(response.data)
    } catch (error) {
      console.error('Failed to load summary:', error)
    }
  }, [])

  useEffect(() => {
    loadControls()
    loadCategories()
    loadSummary()
  }, [scanType, loadControls, loadCategories, loadSummary])

  const filteredControls = controls.filter(control => {
    if (selectedCategory && control.category !== selectedCategory) return false
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      return (
        control.control_id.toLowerCase().includes(query) ||
        control.title.toLowerCase().includes(query) ||
        control.description.toLowerCase().includes(query) ||
        control.category.toLowerCase().includes(query)
      )
    }
    return true
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <BookOpen className="h-7 w-7 text-primary-600" />
            SOC 2 Controls Reference
          </h1>
          <p className="text-gray-500 mt-1">
            Complete guide to SOC 2 Trust Service Criteria
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant={scanType === 'quick' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setScanType('quick')}
          >
            Quick Scan (8)
          </Button>
          <Button 
            variant={scanType === 'full' ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setScanType('full')}
          >
            Full Scan ({summary?.full_scan_count || 50})
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {Object.entries(summary.summary?.categories || {}).map(([category, count]) => (
            <Card key={category} className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setSelectedCategory(selectedCategory === category ? null : category)}>
              <CardContent className="pt-4 pb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">{count as number}</div>
                  <div className="text-xs text-gray-500 mt-1">{category}</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-4">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search controls by ID, title, or description..."
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select
              className="border rounded-lg px-4 py-2 bg-white"
              value={selectedCategory || ''}
              onChange={(e) => setSelectedCategory(e.target.value || null)}
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat.name} value={cat.name}>
                  {cat.name} ({cat.count})
                </option>
              ))}
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Categories Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {categories.map((category) => (
          <Card 
            key={category.name}
            className={`cursor-pointer transition-all ${
              selectedCategory === category.name 
                ? 'ring-2 ring-primary-500 shadow-lg' 
                : 'hover:shadow-md'
            }`}
            onClick={() => setSelectedCategory(
              selectedCategory === category.name ? null : category.name
            )}
          >
            <CardContent className="pt-4">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${categoryColors[category.name] || 'bg-gray-100 text-gray-700'}`}>
                  {categoryIcons[category.name] || <HelpCircle className="h-5 w-5" />}
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">{category.name}</h3>
                  <p className="text-sm text-gray-500">{category.count} controls</p>
                </div>
                <ChevronRight className={`ml-auto h-5 w-5 text-gray-400 transition-transform ${
                  selectedCategory === category.name ? 'rotate-90' : ''
                }`} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Controls List */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>
              Controls 
              {selectedCategory && <span className="text-primary-600 ml-2">• {selectedCategory}</span>}
            </span>
            <Badge variant="info">{filteredControls.length} controls</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : filteredControls.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              No controls found matching your criteria
            </div>
          ) : (
            <div className="space-y-3">
              {filteredControls.map((control) => (
                <div
                  key={control.id}
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    expandedControl === control.control_id
                      ? 'bg-gray-50 border-primary-300'
                      : 'hover:bg-gray-50'
                  }`}
                  onClick={() => setExpandedControl(
                    expandedControl === control.control_id ? null : control.control_id
                  )}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <span className={`font-mono text-sm px-2 py-1 rounded ${
                        categoryColors[control.category] || 'bg-gray-100 text-gray-700'
                      }`}>
                        {control.control_id}
                      </span>
                      <div>
                        <h4 className="font-medium text-gray-900">{control.title}</h4>
                        <p className="text-sm text-gray-500">{control.category}</p>
                      </div>
                    </div>
                    <ChevronRight className={`h-5 w-5 text-gray-400 transition-transform ${
                      expandedControl === control.control_id ? 'rotate-90' : ''
                    }`} />
                  </div>
                  
                  {expandedControl === control.control_id && (
                    <div className="mt-4 pt-4 border-t">
                      <p className="text-sm text-gray-700 mb-4">{control.description}</p>
                      <div className="flex gap-4 text-sm">
                        <div>
                          <span className="text-gray-500">Framework:</span>
                          <span className="ml-2 font-medium">{control.framework}</span>
                        </div>
                        <div>
                          <span className="text-gray-500">Check Type:</span>
                          <span className="ml-2 font-medium">{control.check_type}</span>
                        </div>
                        <div>
                          <span className="text-gray-500">File Types:</span>
                          <span className="ml-2 font-medium">{control.required_file_types}</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Trust Service Categories Explanation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <HelpCircle className="h-5 w-5 text-primary-600" />
            Understanding SOC 2 Trust Service Categories
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">🔒 Security (CC)</h4>
              <p className="text-sm text-blue-700">
                Common Criteria covering access controls, system operations, change management, and risk mitigation.
              </p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-medium text-green-900 mb-2">⚡ Availability (A)</h4>
              <p className="text-sm text-green-700">
                System availability, disaster recovery, backup procedures, and capacity planning.
              </p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <h4 className="font-medium text-purple-900 mb-2">✅ Processing Integrity (PI)</h4>
              <p className="text-sm text-purple-700">
                Data processing accuracy, completeness, and authorization of system outputs.
              </p>
            </div>
            <div className="p-4 bg-orange-50 rounded-lg">
              <h4 className="font-medium text-orange-900 mb-2">🔐 Confidentiality (C)</h4>
              <p className="text-sm text-orange-700">
                Protection of confidential information throughout its lifecycle.
              </p>
            </div>
            <div className="p-4 bg-pink-50 rounded-lg">
              <h4 className="font-medium text-pink-900 mb-2">👤 Privacy (P)</h4>
              <p className="text-sm text-pink-700">
                Collection, use, retention, and disposal of personal information.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
