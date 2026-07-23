export const POST_CATEGORIES = [
  { label: 'Иллюстрации', value: 'artwork' },
  { label: 'Персонажи', value: 'waifu' },
  { label: 'Городские сюжеты', value: 'maid' },
  { label: 'Природа и пейзажи', value: 'nature' },
  { label: 'Фэнтези', value: 'fantasy' },
  { label: 'Портреты', value: 'portrait' },
  { label: 'Архитектура и интерьеры', value: 'architecture' },
  { label: 'Абстракция и эксперименты', value: 'abstract' },
  { label: 'Животные', value: 'animals' },
  { label: 'Еда и натюрморты', value: 'food' },
  { label: 'Технологии и транспорт', value: 'technology' },
  { label: 'Прочее', value: 'other' },
]

export const categoryLabel = (value) =>
  POST_CATEGORIES.find((category) => category.value === value)?.label || value
