using System;
using System.IO;
using System.Security.Cryptography;
using System.Threading;
using System.IO.Compression;
using PgpCore;


namespace cds_poc2
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                // Ensure a path is passed to the application
                Console.WriteLine("Usage: cds_poc2.exe <absolute path of folder to watch>");
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
            // Set filepath and then identify folder being used as the dropbox
            string file_path = e.FullPath.ToString();
            string dropbox = "";
            string[] dropbox_arr = file_path.Split('\\');
            for (int i = 0; i < (dropbox_arr.Length - 1); i++)
            {
                dropbox += dropbox_arr[i];
                if (i < (dropbox_arr.Length - 2))
                    dropbox += "\\";
            }
            // Establish log file for hashes exists within dropbox
            // Then hash the file and write the hash and filename to the log file
            string sha256sum_name = dropbox + "\\sha256sum.txt";
            if (!File.Exists(sha256sum_name))
                File.Create(sha256sum_name);
            Thread.Sleep(TimeSpan.FromSeconds(1));
            string sha_hash = BytesToString(GetChecksum(file_path));
            string line = sha_hash + "\t" + e.Name.ToString();
            using (StreamWriter file = new StreamWriter(sha256sum_name))
                file.WriteLine(line);
            Console.WriteLine("Successfully wrote to " + sha256sum_name);
            Thread.Sleep(TimeSpan.FromSeconds(1));
            // Encrypt file and place it in temp directory within dropbox
            string enc_filename = EncryptFile(file_path, dropbox);
            Thread.Sleep(TimeSpan.FromSeconds(1));
            // Establish path for zipfile output and zip encrypted file along with log file
            string[] zipname_arr = dropbox.Split('\\');
            string zipname = "";
            for (int i = 0; i < (zipname_arr.Length - 1); i++)
            {
                zipname += zipname_arr[i] + "\\";
            }
            zipname += "in_box\\" + GetTimestamp(DateTime.Now) + ".zip";
            string[] enc_parts = enc_filename.Split('\\');
            using (ZipArchive newFile = ZipFile.Open(zipname, ZipArchiveMode.Create))
            {
                newFile.CreateEntryFromFile(enc_filename, enc_parts[enc_parts.Length - 1]);
                newFile.CreateEntryFromFile(sha256sum_name, "sha256sum.txt");
            }
            Console.WriteLine("Successfully zipped files and wrote to " + zipname);
            Thread.Sleep(TimeSpan.FromSeconds(1));
            // Perform cleanup
            File.Delete(file_path);
            File.Delete(enc_filename);
            Console.WriteLine("Cleaning up drop box folder...");
        }
        private static byte[] GetChecksum(string filename)
        {
            // Create SHA256 hash from filestream
            FileStream fileStream = File.OpenRead(filename);
            fileStream.Position = 0;
            var sha = new SHA256Managed();
            byte[] hash = sha.ComputeHash(fileStream);
            fileStream.Close();
            return hash;
        }
        public static string BytesToString(byte[] bytes)
        {
            // Converts byte array to string
            string result = "";
            foreach (byte b in bytes) result += b.ToString("x2");
            return result;
        }
        public static string GetTimestamp(DateTime value)
        {
            // Creates a timestamp
            return value.ToString("yyyyMMddHHmmssfff");
        }
        public static string EncryptFile(string filename, string dropbox)
        {
            using (PGP pgp = new PGP())
            {
                // Encrypt file using keys in the keys directory
                // keys directory must be on the same level of directory structure as the dropbox
                // returns the encrypted filename
                string keydir = "";
                string[] dropbox_arr = dropbox.Split('\\');
                for (int i = 0; i < (dropbox_arr.Length - 1); i++)
                {
                    keydir += dropbox_arr[i] + "\\";
                }
                keydir += "keys\\public.asc";
                string[] fix_filename = filename.Split('\\');
                string enc_filename = dropbox + "\\temp\\" + fix_filename[fix_filename.Length - 1].Split('.')[0] + "_encrypted.pgp";
                pgp.EncryptFile(filename, enc_filename, keydir, true, true);
                Console.WriteLine("Encryption successful");
                return enc_filename;
            }
        }
    }
}
