import { useEffect, useState } from 'react'
import { request, type Room, type RoomDetail } from '../../api/workspace'

export type RoomFile = {
  id: string
  title: string
  version: number
  room: string
}

/** Files of the seller's rooms, so a decision can cite exactly which files it covers. */
export function useSellerFiles(
  companyId: string | null | undefined,
  enabled: boolean,
) {
  const [files, setFiles] = useState<RoomFile[]>([])
  useEffect(() => {
    if (!enabled || !companyId) return
    request<Room[]>(`/rooms?company_id=${companyId}`)
      .then((rooms) =>
        Promise.all(
          rooms.map((room) => request<RoomDetail>(`/rooms/${room.id}`)),
        ),
      )
      .then((details) =>
        setFiles(
          details.flatMap((room) =>
            room.documents.map((document) => ({
              id: document.id,
              title: document.title,
              version: document.current_version,
              room: room.title,
            })),
          ),
        ),
      )
      .catch(() => setFiles([]))
  }, [companyId, enabled])
  return files
}
