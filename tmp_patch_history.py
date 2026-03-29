import re

path = r'c:\Users\phanm\Downloads\220334_TIEN_PHONG_TT_VL_2026\frontend\components\History.tsx'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Find the closing </div> of Image Section (after the flex gap-3 buttons div)
# We look for the pattern: closing </div> of flex gap-3, then closing </div> of space-y-4
# The marker is: Xoá\n                      </button>\n                    </div>\n                 </div>

old_snippet = 'Xo\u00e1\n                      </button>\n                    </div>\n                 </div>'
new_snippet = '''Xo\u00e1
                      </button>
                    </div>
                    {/* N\u00fat chia s\u1ebb c\u1ed9ng \u0111\u1ed3ng */}
                    <button
                      onClick={(e) => handleTogglePublic(selectedBanner, e)}
                      className={`w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold text-sm transition-all ${
                        (selectedBanner.is_public === 1 || selectedBanner.is_public === true)
                          ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border-2 border-emerald-300'
                          : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border-2 border-slate-300'
                      }`}
                    >
                      {(selectedBanner.is_public === 1 || selectedBanner.is_public === true) ? (
                        <><Globe className="h-5 w-5" />\u00a0\u0110ang chia s\u1ebb v\u1edbi C\u1ed9ng \u0111\u1ed3ng \u2014 Nh\u1ea5n \u0111\u1ec3 \u1ea9n</>
                      ) : (
                        <><Lock className="h-5 w-5" />\u00a0\u0110ang Ri\u00eang t\u01b0 \u2014 Nh\u1ea5n \u0111\u1ec3 Chia s\u1ebb C\u1ed9ng \u0111\u1ed3ng</>
                      )}
                    </button>
                 </div>'''

# Normalize line endings for matching
content_normalized = content.replace('\r\n', '\n')
old_normalized = old_snippet.replace('\r\n', '\n')

if old_normalized in content_normalized:
    content_new = content_normalized.replace(old_normalized, new_snippet, 1)
    # Write back with original line endings
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content_new)
    print("SUCCESS: Share button added to modal")
else:
    # Print context around where it should be
    idx = content_normalized.find('Xo\u00e1')
    print(f"NOT FOUND. 'Xoa' at index: {idx}")
    if idx > 0:
        print(repr(content_normalized[idx:idx+200]))
