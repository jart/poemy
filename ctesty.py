import resource
resource.setrlimit(resource.RLIMIT_CORE, (-1, -1))
import sparsehash
sss = sparsehash.SparseStrSet()
sss.add("hello")
sss.add(u"kitty")
sss.add(u"how are you\u3333")
print sss.contains("hello")
print sss.contains("dog")
