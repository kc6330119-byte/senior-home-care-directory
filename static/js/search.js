/**
 * Senior Home Care Finder - Search Functionality
 * Client-side search for agencies using the search-index.json
 */

(function() {
    'use strict';

    let searchIndex = null;
    let isLoading = false;

    /**
     * Load the search index JSON file
     */
    function loadSearchIndex(callback) {
        if (searchIndex) {
            callback(searchIndex);
            return;
        }

        if (isLoading) {
            setTimeout(() => loadSearchIndex(callback), 100);
            return;
        }

        isLoading = true;
        fetch('/search-index.json')
            .then(response => response.json())
            .then(data => {
                searchIndex = data;
                isLoading = false;
                callback(searchIndex);
            })
            .catch(error => {
                console.error('Error loading search index:', error);
                isLoading = false;
            });
    }

    /**
     * Filter agencies based on query
     */
    function filterAgencies(query) {
        if (!searchIndex || query.length < 2) return [];

        const q = query.toLowerCase().trim();
        const results = [];

        for (const agency of searchIndex) {
            const nameMatch = agency.name.toLowerCase().includes(q);
            const cityMatch = agency.city.toLowerCase().includes(q);
            const stateMatch = agency.state.toLowerCase().includes(q);
            const servicesMatch = agency.services && agency.services.some(s => s.toLowerCase().includes(q));

            if (nameMatch || cityMatch || stateMatch || servicesMatch) {
                // Prioritize name matches
                const score = nameMatch ? 3 : (cityMatch ? 2 : (stateMatch ? 1 : 0));
                results.push({ ...agency, score });
            }
        }

        // Sort by score (relevance) and limit to 8 results
        return results
            .sort((a, b) => b.score - a.score)
            .slice(0, 8);
    }

    /**
     * Render search results HTML
     */
    function renderResults(matches) {
        if (matches.length === 0) {
            return '<p class="px-4 py-3 text-sm text-gray-400">No agencies found</p>';
        }

        return matches.map(agency => `
            <a href="/agency/${agency.slug}.html" class="flex items-center gap-3 px-4 py-2.5 hover:bg-primary-50 transition-colors">
                <span class="text-primary-400 text-sm">&#128106;</span>
                <div>
                    <p class="text-sm font-medium text-gray-900">${escapeHtml(agency.name)}</p>
                    <p class="text-xs text-gray-400">${escapeHtml(agency.city)}, ${escapeHtml(agency.state)}</p>
                </div>
            </a>
        `).join('');
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Initialize search functionality
     */
    function initSearch() {
        // Desktop search
        const searchToggle = document.getElementById('search-toggle');
        const searchBox = document.getElementById('search-box');
        const searchInput = document.getElementById('search-input');
        const searchResults = document.getElementById('search-results');

        if (searchToggle && searchBox && searchInput && searchResults) {
            searchToggle.addEventListener('click', function(e) {
                e.stopPropagation();
                searchBox.classList.toggle('hidden');
                if (!searchBox.classList.contains('hidden')) {
                    searchInput.focus();
                    loadSearchIndex(() => {});
                }
            });

            searchInput.addEventListener('input', function() {
                const query = this.value.trim();
                if (query.length < 2) {
                    searchResults.classList.add('hidden');
                    return;
                }
                loadSearchIndex(() => {
                    searchResults.innerHTML = renderResults(filterAgencies(query));
                    searchResults.classList.remove('hidden');
                });
            });

            // Close on outside click
            document.addEventListener('click', function(e) {
                const container = document.getElementById('search-container');
                if (container && !container.contains(e.target)) {
                    searchBox.classList.add('hidden');
                }
            });

            // Close on Escape
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    searchBox.classList.add('hidden');
                }
            });
        }

        // Mobile search
        const mobileInput = document.getElementById('mobile-search-input');
        const mobileResults = document.getElementById('mobile-search-results');

        if (mobileInput && mobileResults) {
            mobileInput.addEventListener('input', function() {
                const query = this.value.trim();
                if (query.length < 2) {
                    mobileResults.classList.add('hidden');
                    return;
                }
                loadSearchIndex(() => {
                    mobileResults.innerHTML = renderResults(filterAgencies(query));
                    mobileResults.classList.remove('hidden');
                });
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSearch);
    } else {
        initSearch();
    }
})();
