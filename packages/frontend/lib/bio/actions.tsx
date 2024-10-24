'use server'

import { auth } from '@/auth'
import { kv } from '@vercel/kv'

interface Links {
  value: string
}
export interface Bio extends Record<string, any> {
  interests: string
  location: string
}

export async function saveBio(bio: Bio) {
  const session = await auth()

  if (session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }
  const userId = 'a4cdb028-6958-4778-8201-1049d0991648'

  try {
    kv.hmset(`user:bio:${userId}`, bio)
  } catch (error) {
    return {
      error: 'Error saving bio'
    }
  }
}

export async function getBio(userId: string) {
  console.log('params', userId)
  const session = await auth()

  if (userId !== session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }

  const _userId = session?.user?.id
  const bio = await kv.hgetall<Bio>(`user:bio:${userId}`)

  return bio
}
