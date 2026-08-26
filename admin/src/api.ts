export type PluginRow = {
  id: number | null;
  name: string;
  type: string;
  image_hard_path: string;
  api_key: string;
  updated_at: string | null;
};

export type PluginDraft = {
  name: string;
  type: string;
  image_hard_path: string;
  api_key: string;
};

// Страница может быть открыта по /admin-x7q2k9 или /admin-x7q2k9/ —
// база для API-запросов берётся из текущего URL
const ADMIN_BASE = location.pathname.replace(/\/+$/, '');

export class Api {
  constructor(private readonly password: string) {}

  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(ADMIN_BASE + (path.startsWith('/') ? path : '/' + path), {
      ...init,
      headers: { 'X-Admin-Password': this.password, ...(init?.headers ?? {}) },
    });
    if (res.status === 401) throw new Error('unauthorized');
    if (!res.ok) throw new Error((await res.text()) || String(res.status));
    if (res.status === 204) return null as T;
    return res.json() as Promise<T>;
  }

  list(): Promise<PluginRow[]> {
    return this.request<PluginRow[]>('api/plugins');
  }

  create(draft: PluginDraft): Promise<PluginRow> {
    return this.request<PluginRow>('api/plugins', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(draft),
    });
  }

  update(id: number, draft: PluginDraft): Promise<PluginRow> {
    return this.request<PluginRow>(`api/plugins/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(draft),
    });
  }

  remove(id: number): Promise<void> {
    return this.request<void>(`api/plugins/${id}`, { method: 'DELETE' });
  }
}
