-- Slugify titles for use in URLs or identifiers.
local function slugify(s)
    return s:gsub("&", "and"):gsub("[%s+/]+", "-"):gsub("[^%w-]+", ""):lower()
end

return {
    Meta = function(m)
        m.slug = m.title and slugify(pandoc.utils.stringify(m.title))
        return m
    end,
}
