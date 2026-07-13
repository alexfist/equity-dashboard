import type { NewsArticle } from "../types";
import { Badge } from "./Badge";
import { fmtUnixDate } from "../lib/format";

export function NewsFeed({ articles }: { articles: NewsArticle[] }) {
  return (
    <div className="rounded-lg border border-panel-border bg-panel p-6">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-text-dim">
          Recent News
        </h3>
        <span className="text-xs text-text-dim">Via Finnhub</span>
      </div>
      {articles.length === 0 ? (
        <p className="py-6 text-center text-sm text-text-dim">No recent news available</p>
      ) : (
        <div className="space-y-4">
          {articles.slice(0, 5).map((a, i) => (
            <div key={i} className="border-t border-panel-border/50 pt-4 first:border-t-0 first:pt-0">
              <div className="mb-1 font-semibold text-text">{a.headline}</div>
              <p className="mb-2 text-sm text-text-dim">{a.summary}</p>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <Badge color="green">{a.source}</Badge>
                <span className="text-text-dim">{fmtUnixDate(a.datetime)}</span>
                <a
                  href={a.url}
                  target="_blank"
                  rel="noreferrer"
                  className="ml-auto font-medium text-accent-blue hover:underline"
                >
                  Read full article →
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
