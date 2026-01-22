import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export function getStatusColor(status: string): string {
  switch (status.toLowerCase()) {
    case 'pass':
      return 'text-green-600 bg-green-100'
    case 'fail':
      return 'text-red-600 bg-red-100'
    case 'needs_review':
      return 'text-yellow-600 bg-yellow-100'
    case 'running':
      return 'text-blue-600 bg-blue-100'
    case 'pending':
      return 'text-gray-600 bg-gray-100'
    case 'succeeded':
      return 'text-green-600 bg-green-100'
    case 'failed':
      return 'text-red-600 bg-red-100'
    default:
      return 'text-gray-600 bg-gray-100'
  }
}

export function getSeverityColor(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'critical':
      return 'text-red-700 bg-red-100 border-red-300'
    case 'high':
      return 'text-orange-700 bg-orange-100 border-orange-300'
    case 'medium':
      return 'text-yellow-700 bg-yellow-100 border-yellow-300'
    case 'low':
      return 'text-blue-700 bg-blue-100 border-blue-300'
    default:
      return 'text-gray-700 bg-gray-100 border-gray-300'
  }
}
