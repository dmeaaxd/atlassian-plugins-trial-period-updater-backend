import './styles.css';

import { Button } from '@consta/uikit/Button';
import { ChoiceGroup } from '@consta/uikit/ChoiceGroup';
import { Text } from '@consta/uikit/Text';
import { TextField } from '@consta/uikit/TextField';
import { useEffect, useState } from 'react';

import { Api, type PluginRow } from './api';

const typeItems = [
  { label: 'Jira', value: 'JIRA' },
  { label: 'Confluence', value: 'CONFLUENCE' },
];

const fmtMsk = (value: string | null): string => {
  if (!value) return '—';
  return (
    new Date(value + 'Z').toLocaleString('ru-RU', {
      timeZone: 'Europe/Moscow',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }) + ' MSK'
  );
};

// Ключ всегда хранится одной строкой — переносы вырезаются даже при вставке
const normalizeKey = (key: string): string => key.replace(/[\r\n]+/g, '').trim();

const newRow = (): PluginRow => ({
  id: null,
  name: '',
  type: 'JIRA',
  image_hard_path: 'icons/jira_plugins/',
  api_key: '',
  updated_at: null,
});

const errorMessage = (e: unknown): string =>
  e instanceof Error && e.message === 'unauthorized' ? 'Неверный пароль' : String((e as Error)?.message ?? e);

export const App = () => {
  const [password, setPassword] = useState('');
  const [api, setApi] = useState<Api | null>(null);
  const [rows, setRows] = useState<PluginRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<number | 'new' | null>(null);

  useEffect(() => {
    if (!api) return;
    setLoading(true);
    api
      .list()
      .then((plugins) => {
        setRows(plugins.map((p) => ({ ...p, api_key: normalizeKey(p.api_key) })));
        setError(null);
      })
      .catch((e) => setError(errorMessage(e)))
      .finally(() => setLoading(false));
  }, [api]);

  const login = async () => {
    setError(null);
    const candidate = new Api(password);
    try {
      await candidate.list();
      setApi(candidate);
      setPassword('');
    } catch (e) {
      setError(errorMessage(e));
    }
  };

  const updateRow = (id: number | null, patch: Partial<PluginRow>) =>
    setRows((rs) => rs.map((r) => (r.id === id ? { ...r, ...patch } : r)));

  const saveRow = async (row: PluginRow) => {
    setSaving(row.id ?? 'new');
    setError(null);
    try {
      const draft = {
        name: row.name.trim(),
        type: row.type,
        image_hard_path: row.image_hard_path.trim(),
        api_key: normalizeKey(row.api_key),
      };
      const saved = row.id ? await api!.update(row.id, draft) : await api!.create(draft);
      setRows((rs) =>
        row.id
          ? rs.map((r) => (r.id === row.id ? { ...saved, api_key: normalizeKey(saved.api_key) } : r))
          : [{ ...saved, api_key: normalizeKey(saved.api_key) }, ...rs.filter((r) => r.id !== null)]
      );
    } catch (e) {
      setError(errorMessage(e));
    } finally {
      setSaving(null);
    }
  };

  const deleteRow = async (row: PluginRow) => {
    if (row.id === null) {
      setRows((rs) => rs.filter((r) => r.id !== null));
      return;
    }
    if (!window.confirm(`Удалить плагин «${row.name}»?`)) return;
    setError(null);
    try {
      await api!.remove(row.id);
      setRows((rs) => rs.filter((r) => r.id !== row.id));
    } catch (e) {
      setError(errorMessage(e));
    }
  };

  const addRow = () =>
    setRows((rs) => (rs.some((r) => r.id === null) ? rs : [newRow(), ...rs]));

  const lastUpdate = rows.reduce<string | null>(
    (max, r) => (r.updated_at && (!max || r.updated_at > max) ? r.updated_at : max),
    null
  );

  if (!api) {
    return (
      <div className="admin-login">
        <Text size="l" weight="bold" as="h1">
          Админка
        </Text>
        <TextField
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(v) => setPassword(v ?? '')}
          onKeyDown={(e) => {
            if (e.key === 'Enter') login();
          }}
        />
        <Button label="Войти" view="primary" onClick={login} />
        {error && (
          <Text view="alert" size="s">
            {error}
          </Text>
        )}
      </div>
    );
  }

  return (
    <div className="admin">
      <div className="admin-header">
        <Text size="l" weight="bold" as="h1">
          Плагины
        </Text>
        <Text size="s" view="secondary">
          Последнее обновление базы: {fmtMsk(lastUpdate)}
        </Text>
      </div>

      {error && (
        <Text view="alert" size="s">
          {error}
        </Text>
      )}

      <div className="admin-table">
        <div className="admin-grid admin-grid--head">
          <Text size="xs" view="secondary">
            Название
          </Text>
          <Text size="xs" view="secondary">
            Тип
          </Text>
          <Text size="xs" view="secondary">
            Путь к иконке
          </Text>
          <Text size="xs" view="secondary">
            API-ключ
          </Text>
          <Text size="xs" view="secondary">
            Обновлён (МСК)
          </Text>
          <div />
        </div>

        {loading && rows.length === 0 ? (
          <Text size="m">Загрузка...</Text>
        ) : (
          rows.map((row) => (
            <div className="admin-grid" key={row.id ?? 'new'}>
              <TextField
                value={row.name}
                onChange={(v) => updateRow(row.id, { name: v ?? '' })}
                placeholder="Название"
              />
              <ChoiceGroup
                name={'type-' + (row.id ?? 'new')}
                items={typeItems}
                value={typeItems.find((t) => t.value === row.type) ?? typeItems[0]}
                onChange={(item) => updateRow(row.id, { type: String(item.value) })}
                getItemLabel={(item) => item.label}
                width="full"
              />
              <TextField
                value={row.image_hard_path}
                onChange={(v) => updateRow(row.id, { image_hard_path: v ?? '' })}
                placeholder="icons/..."
              />
              <TextField
                value={row.api_key}
                onChange={(v) => updateRow(row.id, { api_key: normalizeKey(v ?? '') })}
                placeholder="API-ключ (одной строкой)"
              />
              <Text size="s" view="secondary" className="admin-date">
                {fmtMsk(row.updated_at)}
              </Text>
              <div className="admin-actions">
                <Button
                  label="Сохранить"
                  view="primary"
                  disabled={saving !== null}
                  onClick={() => saveRow(row)}
                />
                <Button label="Удалить" view="ghost" onClick={() => deleteRow(row)} />
              </div>
            </div>
          ))
        )}
      </div>

      <div className="admin-add">
        <Button label="+ Добавить плагин" view="primary" onClick={addRow} />
      </div>
    </div>
  );
};
