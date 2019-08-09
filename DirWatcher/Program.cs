using System;
using System.IO;
using System.Threading;


namespace dirwatcher
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                // Ensure a path is passed to the application
                Console.WriteLine("Usage: dirwatcher.exe <absolute path of folder to watch>");
                System.Environment.Exit(1);
            }
            else
            {
                // Build watcher, set filters, and watch for file creation
                FileSystemWatcher fsw = new FileSystemWatcher(args[0]);
                fsw.NotifyFilter = NotifyFilters.LastAccess | NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName;
                fsw.Created += new FileSystemEventHandler(OnCreate);
                Console.WriteLine("Begin watching " + args[0] + "...");
                fsw.EnableRaisingEvents = true;
                // Exit on Enter key
                Console.WriteLine("Press \'Enter\' to quit...");
                Console.ReadLine();
            }
        }
        private static void OnCreate(object source, FileSystemEventArgs e)
        {
            // Set filepath and then identify folder being watched
            string file_path = e.FullPath.ToString();
            Console.WriteLine("File written to path: " + file_path);
            Thread.Sleep(TimeSpan.FromSeconds(1));
        }
        
    }
}
