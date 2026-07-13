type BadgeColor = "blue" | "green" | "gray" | "amber";

const COLOR_CLASSES: Record<BadgeColor, string> = {
  blue: "bg-accent-blue/15 text-accent-blue",
  green: "bg-accent-green/15 text-accent-green",
  gray: "bg-white/10 text-text-dim",
  amber: "bg-accent-amber/15 text-accent-amber",
};

export function Badge({ color, children }: { color: BadgeColor; children: React.ReactNode }) {
  return (
    <span className={`inline-block rounded px-2 py-0.5 text-xs font-medium ${COLOR_CLASSES[color]}`}>
      {children}
    </span>
  );
}
