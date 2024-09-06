local function slugify(s)
	return s:gsub("[%s+/]+", "-"):gsub("[^%w-]+", ""):lower()
end

return {
	Meta = function(m)
		m.slug = m.title and slugify(pandoc.utils.stringify(m.title))
		return m
	end,
}
