import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/axios'
import type {
  Job,
  JobListResponse,
  CreateJobRequest,
  EvidenceListResponse,
  GapListResponse,
} from '../types'

export function useJobs() {
  return useQuery({
    queryKey: ['jobs'],
    queryFn: async () => {
      const response = await api.get<JobListResponse>('/jobs')
      return response.data
    },
  })
}

export function useJob(jobId: string) {
  return useQuery({
    queryKey: ['jobs', jobId],
    queryFn: async () => {
      const response = await api.get<Job>(`/jobs/${jobId}`)
      return response.data
    },
    refetchInterval: (query) => {
      // Poll every 2 seconds if job is still running
      const data = query.state.data
      if (data?.status === 'RUNNING' || data?.status === 'PENDING') {
        return 2000
      }
      return false
    },
  })
}

export function useJobEvidence(jobId: string) {
  return useQuery({
    queryKey: ['jobs', jobId, 'evidence'],
    queryFn: async () => {
      const response = await api.get<EvidenceListResponse>(
        `/jobs/${jobId}/evidence`
      )
      return response.data
    },
  })
}

export function useJobGaps(jobId: string) {
  return useQuery({
    queryKey: ['jobs', jobId, 'gaps'],
    queryFn: async () => {
      const response = await api.get<GapListResponse>(`/jobs/${jobId}/gaps`)
      return response.data
    },
  })
}

export function useCreateJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateJobRequest) => {
      const response = await api.post<Job>('/jobs/evidence-run', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
  })
}

export function useDeleteJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (jobId: string) => {
      await api.delete(`/jobs/${jobId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
    },
  })
}

export function useRunJob() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (jobId: string) => {
      const response = await api.post<Job>(`/jobs/${jobId}/run`)
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] })
      queryClient.invalidateQueries({ queryKey: ['jobs', data.id] })
    },
  })
}
