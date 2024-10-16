import { format, parseISO } from 'lib/utils'

interface Event {
  date: string
  link: string
  title: string
}

// TODO: Extract date in API Call from server

export function Events({ props: events }: { props: Event[] }) {
  return (
    <div className="-mt-2 flex w-full flex-col gap-2 py-4">
      {events.map(event => (
        <a href={event.link} target="_">
          <div
            key={event?.date}
            className="flex shrink-0 flex-col gap-1 rounded-lg bg-zinc-800 p-4"
          >
            <div className="text-sm text-zinc-400">
              {format(parseISO(event?.date), 'dd LLL, yyyy')}
            </div>
            <div className="text-base font-bold text-zinc-200">
              {event.title}
            </div>
            {/* <div className="text-zinc-500">
            {event.description.slice(0, 70)}...
          </div> */}
          </div>
        </a>
      ))}
    </div>
  )
}
