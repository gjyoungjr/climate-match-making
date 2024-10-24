'use server'

import { auth } from '@/auth'
import { kv } from '@vercel/kv'

interface Links {
  [key: string]: string
}
interface Bio extends Record<string, any> {
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
  const userId = session?.user?.id

  try {
    const pipeline = kv.pipeline()

    pipeline.hmset(`user:${userId}:bio`, bio)
    await pipeline.exec()
  } catch (error) {
    return {
      error: 'Error saving bio'
    }
  }
}

export async function getBio(userId: string) {
  const session = await auth()

  if (userId !== session?.user?.id) {
    return {
      error: 'Unauthorized'
    }
  }

  const _userId = session?.user?.id
  const bio = await kv.hgetall<Bio>(`user:${_userId}:bio`)

  return bio
}
