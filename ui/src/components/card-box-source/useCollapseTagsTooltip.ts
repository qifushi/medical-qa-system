import { ref, computed } from 'vue';

export function useCollapseTagsTooltip(tags: string[], maxVisible: number = 5) {
  const isEllipsis = computed(() => tags && tags.length > maxVisible);
  const visibleTags = computed(() => {
    if (!tags) return [];
    return isEllipsis.value
      ? [...tags.slice(0, maxVisible - 1), tags.slice(maxVisible - 1).join(',')]
      : tags;
  });
  const ellipsisContent = computed(() => {
    if (!tags) return '';
    console.log('[ tags ] >', tags)
    return tags.slice(maxVisible - 1).join(',');
  });

  return {
    isEllipsis,
    visibleTags,
    ellipsisContent
  };
}