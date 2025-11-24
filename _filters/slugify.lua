-- Slugify titles for use in URLs or identifiers.
local function slugify(s)
    -- Convert ampersand to and
    s = s:gsub("&", "and")
    -- Convert spaces/slashes to hyphens
    s = s:gsub("[%s+/]+", "-")
    -- Remove non-alphanumeric/non-hyphen characters and convert to lowercase
    return s:gsub("[^%w-]+", ""):lower()
end

return {
    Meta = function(m)
        m.slug = m.title and slugify(pandoc.utils.stringify(m.title))
        return m
    end,
}
