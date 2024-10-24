'use client'

import Link from 'next/link'
import { zodResolver } from '@hookform/resolvers/zod'
import { useFieldArray, useForm } from 'react-hook-form'
import { z } from 'zod'
import React from 'react'
import { cn } from '@/lib/utils'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Separator } from '@/components/ui/separator'
import { Session } from '@/lib/types'
import { auth } from '@/auth'

const profileFormSchema = z.object({
  location: z.string({
    required_error: 'Please enter your city.'
  }),
  interest: z.string().max(160).min(4),
  urls: z
    .array(
      z.object({
        value: z.string().url({ message: 'Please enter a valid URL.' })
      })
    )
    .optional()
})

type ProfileFormValues = z.infer<typeof profileFormSchema>

// This can come from your database or API.
const defaultValues: Partial<ProfileFormValues> = {
  interest: ''
}

export default function ProfileForm() {
  const form = useForm<ProfileFormValues>({
    resolver: zodResolver(profileFormSchema),
    defaultValues,
    mode: 'onChange'
  })

  const { fields, append } = useFieldArray({
    name: 'urls',
    control: form.control
  })

  function onSubmit(data: ProfileFormValues) {
    alert(JSON.stringify(data, null, 2))
    // // toast({
    // //   title: 'You submitted the following values:',
    // //   description: (
    // //     <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
    // //       <code className="text-white">{JSON.stringify(data, null, 2)}</code>
    // //     </pre>
    // //   )
    // // })
    // toast.success('Profile updated!')
    ;<div>hey</div>
  }

  React.useEffect(() => {
    console.log('session')

    // Define the async function inside the useEffect
    const fetchSession = async () => {
      try {
        const session = (await auth()) as Session
        console.log('session')
      } catch (error) {
        console.error('Failed to fetch session:', error)
      }
    }

    // Call the async function
    fetchSession()
  }, [])

  return (
    <div className="space-y-6 ml-20 mr-20 mt-10">
      <div className="space-y-0.5">
        <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">Manage your account settings.</p>
      </div>
      <Separator />
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="location"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Location</FormLabel>
                <FormControl>
                  <Input placeholder="San Francisco" {...field} />
                </FormControl>
                <FormDescription>What city are you based in?</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="interest"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Interests</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="Tell us what are you working on."
                    className="resize-none"
                    {...field}
                  />
                </FormControl>
                <FormDescription>
                  i.e I'm building AI hardware for carbon sequestration.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
          <div>
            {fields.map((field, index) => (
              <FormField
                control={form.control}
                key={field.id}
                name={`urls.${index}.value`}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className={cn(index !== 0 && 'sr-only')}>
                      URLs
                    </FormLabel>
                    <FormDescription className={cn(index !== 0 && 'sr-only')}>
                      Add links to your website, blog, or social media profiles.
                    </FormDescription>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            ))}
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="mt-2"
              onClick={() => append({ value: '' })}
            >
              Add URL
            </Button>
          </div>
          <Button type="submit">Update profile</Button>
        </form>
      </Form>
    </div>
  )
}
