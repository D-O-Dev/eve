// index.ts
import { en } from "./en";
import { fr } from "./fr";

export type Locale = "fr" | "en";
export type MessageKey = keyof typeof fr;

const dictionaries = { fr, en };

export function t(key: MessageKey, params?: Record<string, string | number>, locale: Locale = "fr"): string {
  let text: string = dictionaries[locale][key];
  if (params) {
    for (const [name, value] of Object.entries(params)) {
      text = text.replaceAll(`{${name}}`, String(value));
    }
  }
  return text;
}