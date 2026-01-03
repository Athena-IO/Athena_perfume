<script setup>
import { useEditor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Image from "@tiptap/extension-image";
import Placeholder from "@tiptap/extension-placeholder";

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "توضیحات محصول را وارد کنید...",
  },
});

const emit = defineEmits(["update:modelValue"]);

const editor = useEditor({
  extensions: [
    StarterKit,
    Image.configure({
      inline: true,
      allowBase64: true,
    }),
    Placeholder.configure({
      placeholder: props.placeholder,
    }),
  ],
  content: props.modelValue,
  onUpdate: ({ editor }) => {
    try {
      emit("update:modelValue", editor.getHTML());
    } catch (error) {
      console.warn('Error updating editor content:', error);
    }
  },
  editorProps: {
    attributes: {
      class: "prose prose-sm max-w-none focus:outline-none min-h-[200px] p-4",
    },
    handleDOMEvents: {
      focus: (view, event) => {
        try {
          return true;
        } catch (error) {
          console.warn('Focus event error:', error);
          return true;
        }
      },
      blur: (view, event) => {
        try {
          return true;
        } catch (error) {
          console.warn('Blur event error:', error);
          return true;
        }
      },
    },
  },
});

watch(
  () => props.modelValue,
  (value) => {
    if (editor.value && value !== editor.value.getHTML()) {
      editor.value.commands.setContent(value, false);
    }
  }
);

onBeforeUnmount(() => {
  editor.value?.destroy();
});

const addImage = () => {
  if (process.client) {
    const url = window.prompt("آدرس تصویر را وارد کنید:");

    if (url) {
      editor.value?.chain().focus().setImage({ src: url }).run();
    }
  }
};

const uploadImage = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  // Convert to base64
  const reader = new FileReader();
  reader.onload = (e) => {
    const base64 = e.target?.result;
    if (base64) {
      editor.value?.chain().focus().setImage({ src: base64 }).run();
    }
  };
  reader.readAsDataURL(file);
};

const toolbarActions = [
  {
    icon: "i-lucide-bold",
    title: "Bold",
    action: () => editor.value?.chain().focus().toggleBold().run(),
    isActive: () => editor.value?.isActive("bold"),
  },
  {
    icon: "i-lucide-italic",
    title: "Italic",
    action: () => editor.value?.chain().focus().toggleItalic().run(),
    isActive: () => editor.value?.isActive("italic"),
  },
  {
    icon: "i-lucide-strikethrough",
    title: "Strike",
    action: () => editor.value?.chain().focus().toggleStrike().run(),
    isActive: () => editor.value?.isActive("strike"),
  },
  {
    icon: "i-lucide-heading-1",
    title: "Heading 1",
    action: () =>
      editor.value?.chain().focus().toggleHeading({ level: 1 }).run(),
    isActive: () => editor.value?.isActive("heading", { level: 1 }),
  },
  {
    icon: "i-lucide-heading-2",
    title: "Heading 2",
    action: () =>
      editor.value?.chain().focus().toggleHeading({ level: 2 }).run(),
    isActive: () => editor.value?.isActive("heading", { level: 2 }),
  },
  {
    icon: "i-lucide-list",
    title: "Bullet List",
    action: () => editor.value?.chain().focus().toggleBulletList().run(),
    isActive: () => editor.value?.isActive("bulletList"),
  },
  {
    icon: "i-lucide-list-ordered",
    title: "Ordered List",
    action: () => editor.value?.chain().focus().toggleOrderedList().run(),
    isActive: () => editor.value?.isActive("orderedList"),
  },
  {
    icon: "i-lucide-quote",
    title: "Blockquote",
    action: () => editor.value?.chain().focus().toggleBlockquote().run(),
    isActive: () => editor.value?.isActive("blockquote"),
  },
  {
    icon: "i-lucide-code",
    title: "Code Block",
    action: () => editor.value?.chain().focus().toggleCodeBlock().run(),
    isActive: () => editor.value?.isActive("codeBlock"),
  },
  {
    icon: "i-lucide-undo",
    title: "Undo",
    action: () => editor.value?.chain().focus().undo().run(),
    isActive: () => false,
  },
  {
    icon: "i-lucide-redo",
    title: "Redo",
    action: () => editor.value?.chain().focus().redo().run(),
    isActive: () => false,
  },
];
</script>

<template>
  <div
    v-if="editor"
    class="border border-default rounded-lg overflow-hidden bg-default"
  >
    <!-- Toolbar -->
    <div
      class="flex flex-wrap items-center gap-1 p-2 border-b border-default bg-elevated"
    >
      <button
        v-for="(action, index) in toolbarActions"
        :key="index"
        type="button"
        :title="action.title"
        class="p-2 rounded hover:bg-default transition-colors"
        :class="{ 'bg-primary/10 text-primary': action.isActive() }"
        @click="action.action"
      >
        <UIcon :name="action.icon" class="size-4" />
      </button>

      <!-- Divider -->
      <div class="h-6 w-px bg-default mx-1" />

      <!-- Image Upload -->
      <label
        title="Upload Image"
        class="p-2 rounded hover:bg-default transition-colors cursor-pointer"
      >
        <UIcon name="i-lucide-image-plus" class="size-4" />
        <input
          type="file"
          accept="image/*"
          class="hidden"
          @change="uploadImage"
        />
      </label>

      <!-- Image URL -->
      <button
        type="button"
        title="Add Image URL"
        class="p-2 rounded hover:bg-default transition-colors"
        @click="addImage"
      >
        <UIcon name="i-lucide-link" class="size-4" />
      </button>
    </div>

    <!-- Editor -->
    <EditorContent :editor="editor" />
  </div>
</template>

<style>
.ProseMirror {
  min-height: 200px;
}

.ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}

.ProseMirror img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1rem 0;
}
</style>
