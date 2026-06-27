type HeaderProps = {
  title: string;
};

export default function Header({ title }: HeaderProps) {
  return (
    <header className="flex items-center justify-center">
      <h1 className="text-2xl font-bold">{title}</h1>
    </header>
  );
}