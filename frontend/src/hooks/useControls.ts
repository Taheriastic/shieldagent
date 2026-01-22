import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/axios'
import type { ControlListResponse } from '../types'

export function useControls(framework: string = 'soc2') {
  return useQuery({
    queryKey: ['controls', framework],
    queryFn: async () => {
      const response = await api.get<ControlListResponse>(
        `/controls?framework=${framework}`
      )
      return response.data
    },
    staleTime: 1000 * 60 * 60, // 1 hour - controls don't change often
  })
}
