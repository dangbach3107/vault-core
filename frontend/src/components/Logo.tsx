type LogoProps = {
  /** `color` for light surfaces, `white` for dark/red surfaces, `mark` for the icon only. */
  variant?: 'color' | 'white' | 'mark'
  /** Rendered height in px; width follows the aspect ratio (196:64 lockup, 1:1 mark). */
  height?: number
  className?: string
}

const sources = {
  color: '/logo/vault-a-lockup.svg',
  white: '/logo/vault-a-lockup-white.svg',
  mark: '/logo/vault-a-mark.svg',
} as const

export default function Logo({
  variant = 'color',
  height = 32,
  className = '',
}: LogoProps) {
  return (
    <img
      className={`vault-logo ${className}`.trim()}
      src={sources[variant]}
      alt="VAULT"
      height={height}
      width={Math.round(variant === 'mark' ? height : (height * 196) / 64)}
      draggable={false}
    />
  )
}
