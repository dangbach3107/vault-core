export type LegalKind = 'terms' | 'privacy' | 'contact'

export const legalPaths: Record<string, LegalKind> = {
  '/terms': 'terms',
  '/privacy': 'privacy',
  '/contact': 'contact',
}
