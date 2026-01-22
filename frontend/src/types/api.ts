// API Types - matching backend Pydantic schemas

export interface User {
  id: string
  email: string
  full_name: string | null
  is_active: boolean
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface Document {
  id: string
  filename: string
  original_filename: string
  file_type: string
  file_size: number
  uploaded_at: string
  metadata: Record<string, unknown> | null
}

export interface DocumentListResponse {
  documents: Document[]
  total: number
}

export interface Job {
  id: string
  job_type: string
  scan_type?: 'quick' | 'full'
  status: 'PENDING' | 'RUNNING' | 'SUCCEEDED' | 'FAILED' | 'CANCELLED'
  progress: number
  total_controls: number
  error_message: string | null
  started_at: string | null
  completed_at: string | null
  created_at: string
}

export interface JobListResponse {
  jobs: Job[]
  total: number
}

export interface Control {
  id: string
  control_id: string
  framework: string
  title: string
  description: string
  check_type: 'ai_prompt' | 'deterministic'
  category: string
  required_file_types: string | null
}

export interface ControlListResponse {
  controls: Control[]
  total: number
}

export interface EvidenceItem {
  id: string
  job_id: string
  control_id: string
  status: 'pass' | 'fail' | 'needs_review' | 'not_applicable' | 'error'
  confidence: number
  summary: string | null
  evidence_quote: string | null
  source_location: string | null
  source_document_ids: string[] | null
  evidence_metadata: Record<string, unknown> | null
  created_at: string
}

export interface EvidenceListResponse {
  evidence_items: EvidenceItem[]
  total: number
  passing: number
  failing: number
  needs_review: number
}

export interface Gap {
  id: string
  job_id: string
  control_id: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  description: string
  remediation_suggestion: string | null
  created_at: string
}

export interface GapListResponse {
  gaps: Gap[]
  total: number
  by_severity: Record<string, number>
}

// Request types
export interface RegisterRequest {
  email: string
  password: string
  full_name?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface CreateJobRequest {
  framework: string
  document_ids: string[]
  scan_type?: 'quick' | 'full'
}

// API Error
export interface ApiError {
  detail: string
}
