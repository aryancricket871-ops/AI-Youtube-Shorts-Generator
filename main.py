                description=metadata['description'],
                tags=metadata['tags'],
                privacy_status=args.privacy,
            )
        except Exception as e:
            # The video rendered fine; a failed upload should not discard it.
            print(f"❌ Upload Error: {e}")

    if final_path and not args.keep_cache:
        clean_cache()

    return final_path


async def main_async(args):
    if args.check:
        problems = preflight(args)
        for problem in problems:
            print(f"❌ {problem}")
        if problems:
            return 1
        print("✅ Preflight passed — ready to run.")
        return 0

    problems = preflight(args)
    if problems:
